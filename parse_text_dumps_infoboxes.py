import argparse
import bz2
import csv
import os
import re

import mwparserfromhell
import mwxml


def get_page_properties(output_fn, dump_date, langs):
    """Get some basic page properties for pages in various Wikipedia language editions.

    NOTES:
        * When I actually ran this, I also limited the output to a set of page-IDs by checking `page.id` against a whitelist
        *
    """
    
    
    redirects = {}
    infobox_settlements = []
    
    with open('infobox-settlement-titles.list') as fin:
        next(fin)
        for line in fin:
            infobox_settlements.append(line.rstrip('\n').replace('_', ' '))

    print(infobox_settlements)
    print("SETTLEMENT INFOBOXES:\n")
    for i_s in infobox_settlements:
        print(i_s + "\n")
    print("\n")
            
    with open(output_fn, 'w') as fout:
        tsvwriter = csv.writer(fout, delimiter='\t')
        header = ['lang', 'title', 'page_id', 'rev_id', 'settlement']
        tsvwriter.writerow(header)
        for lang in langs:
            print("\n====={0}=====".format(lang))
            dump_fn = build_local_currentpage_dump_fn(lang, dump_date)
            kept = 0
            with bz2.BZ2File(dump_fn) as fin:
                dump_iter = mwxml.Dump.from_file(fin)
                for processsed, page in enumerate(dump_iter, start=1):
                    # I was only interested in main namespace articles (change to 1 for talk pages)
                    if page.namespace == 0:
                        title = page.title
                        pid = page.id
                        rev = next(page)
                        try:
                            wikitext = mwparserfromhell.parse(rev.text)
                            page_length = len(wikitext)
                            content_length = len(wikitext.strip_code())
                        except Exception:
                            print("Skipping: {0}".format(pid))
                            continue
                        templates = wikitext.filter_templates()
                        # templates_all = []
                        settlement = ""
                        for template in templates:
                            template_name = str(template.name).strip().replace("_", " ")
                            template_name = template_name[0].upper() + template_name[1:]
                            # templates_all.append(template_name)
                            if template_name in infobox_settlements:
                                subdivision_type = "unknown_subdivision_type"
                                if template.has("subdivision_type"):
                                    cleaned = template.get("subdivision_type").value.strip()
                                    subdivision_type = cleaned if cleaned else "unknown_subdivision_type"
                                subdivision_name = "unknown_subdivision_name"
                                if template.has("subdivision_name"):
                                    cleaned = template.get("subdivision_name").value.strip()
                                    subdivision_name = cleaned if cleaned else "uknown_subdivision_name"
                                settlement = template_name + "~~~" + subdivision_type + "~~~" + subdivision_name
                                # print(title + " : " + template_name + " : " + subdivision_type + " : " + subdivision_name)
                                break
                        if not settlement:
                            continue
                        # templates_all_concat = "!!!".join(templates_all) if len(templates) else "no_templates"
                        tsvwriter.writerow([lang, title, pid, rev.id, settlement])
                        kept += 1
                        if kept % 1000 == 0:
                            print('{0}:\t{1} of {2} lines written.'.format(lang, kept, processsed))
    print('{0}:\t{1} of {2} lines written.'.format(lang, kept, processsed))


def build_local_currentpage_dump_fn(lang='en', date='20191201'):
    """Get dump filepath on stat100X based on date and language"""
    local_replicas = '/mnt/data/xmldatadumps/public'
    # a few small hacks to deal with quirks of my data
    lang = lang.replace('-', '_')
    if lang == 'be_tarask':
        lang = 'be_x_old'
    return os.path.join(local_replicas, '{0}wiki'.format(lang), date, '{0}wiki-{1}-pages-articles.xml.bz2'.format(lang, date))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output_fn", help="TSV file to write page properties.")
    parser.add_argument("--dump_date", default="20191201", help="Dump date in format YYYYMMDD")
    parser.add_argument("--langs", nargs="*", default=['en'], help='Wikis to process -- e.g., "en fr fa"')
    args = parser.parse_args()

    get_page_properties(args.output_fn, args.dump_date, args.langs)

