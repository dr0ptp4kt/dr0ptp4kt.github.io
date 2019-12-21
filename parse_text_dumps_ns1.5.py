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
        * adapted from isaacj script
    """
    
    
    redirects = {}
    with open('wikiproject_redirects_ns1.5.tsv') as fin:
        tsv_reader = csv.reader(fin, delimiter='\t')
        column_names = next(tsv_reader)
        for line in tsv_reader:
            redirects[line[0].replace("_", " ")] = line[1].replace("_", " ")

    for item in redirects.items():
        print(item)

    with open(output_fn, 'w') as fout:
        tsvwriter = csv.writer(fout, delimiter='\t')
        header = ['lang', 'title', 'page_id', 'rev_id', 'page_length', 'content_length',
                  'num_headings_2', 'num_headings_3p',
                  'num_templates', 'num_refs', 'num_wikilinks', 'num_extlinks', 'wikiproject_templates']
        tsvwriter.writerow(header)
        for lang in langs:
            print("\n====={0}=====".format(lang))
            dump_fn = build_local_currentpage_dump_fn(lang, dump_date)
            kept = 0
            with bz2.BZ2File(dump_fn) as fin:
                dump_iter = mwxml.Dump.from_file(fin)
                for processsed, page in enumerate(dump_iter, start=1):
                    # I was only interested in main namespace articles (change to 1 for talk pages)
                    if page.namespace == 1:
                        title = page.title
                        pid = page.id
                        rev = next(page)
                        try:
                            wikitext = mwparserfromhell.parse(rev.text)
                            page_length = len(wikitext)
                            content_length = len(wikitext.strip_code())
                        except Exception:
                            print("Skipping malformed parse: {0}".format(pid))
                            continue
                        headings = wikitext.filter_headings()
                        headings_levtwo = sum([1 for l in headings if l.count('=') == 4])
                        headings_levthrpls = sum([1 for l in headings if l.count('=') >= 6])
                        templates = wikitext.filter_templates()
                        num_templates = len(templates)
                        wikiproject_templates = []
                        for template in templates:
                            template_name = mwparserfromhell.parse(str(template.name).strip()).strip_code().replace("_", " ")
                            try:
                                template_name = template_name[0].upper() + template_name[1:]
                            except Exception:
                                print("Skipping malformed template: pid {0}: {1}".format(pid, template))
                                continue
                            # if template_name in redirects:
                            #    print (title + " : " + template_name + " : " + redirects[template_name])
                            template_name = redirects[template_name] if template_name in redirects else template_name
                            if (re.match('^wikiproject ', template_name, re.I)):
                                importance = "unknown_importance"
                                if template.has("importance") :
                                    cleaned = template.get("importance").value.strip()
                                    cleaned = mwparserfromhell.parse(template.get("importance").value.strip()).strip_code()
                                    importance = cleaned.lower() if cleaned else "unknown_importance"
                                wikiproject_templates.append(template_name + "~~~" + importance)
                        wikiproject_templates_all = "!!!".join(wikiproject_templates) if len(wikiproject_templates) else "no_wikiprojects"
                        num_refs = sum([1 for t in wikitext.ifilter_tags() if t.tag == 'ref'])
                        num_wikilinks = len(wikitext.filter_wikilinks())
                        num_extlinks = len(wikitext.filter_external_links())
                        tsvwriter.writerow([lang, title, pid, rev.id, page_length, content_length,
                                            headings_levtwo, headings_levthrpls,
                                            num_templates, num_refs, num_wikilinks, num_extlinks, wikiproject_templates_all])
                        kept += 1
                        if kept % 1000 == 0:
                            print('{0}:\t{1} of {2} lines written.'.format(lang, kept, processsed))
    print('{0}:\t{1} of {2} lines written.'.format(lang, kept, processsed))


def build_local_currentpage_dump_fn(lang='en', date='20191201'):
    """Get dump filepath on stat100X based on date and language"""
    #local_replicas = '/mnt/data/xmldatadumps/public/{0}wiki/{1}'.format(lang, date)
    local_replicas = '/mnt/data/xmldatadumps/public'
    # a few small hacks to deal with quirks of my data
    lang = lang.replace('-', '_')
    if lang == 'be_tarask':
        lang = 'be_x_old'
    return os.path.join(local_replicas, '{0}wiki'.format(lang), date, '{0}wiki-{1}-pages-meta-current.xml.bz2'.format(lang, date))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output_fn", help="TSV file to write page properties.")
    parser.add_argument("--dump_date", default="20191201", help="Dump date in format YYYYMMDD")
    parser.add_argument("--langs", nargs="*", default=['en'], help='Wikis to process -- e.g., "en fr fa"')
    args = parser.parse_args()

    get_page_properties(args.output_fn, args.dump_date, args.langs)
