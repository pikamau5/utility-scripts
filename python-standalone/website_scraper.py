import requests
from bs4 import BeautifulSoup


def get_first_vex_function_usage(url, out_path):
    # Fetch the content of the main VEX functions page
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all links with the specified class
    function_links = soup.find_all('a', class_='label-text vex')


    # Check if there are any function links found
    if not function_links:
        return "No VEX function links found."

    descs = []
    links = []
    for item in function_links:
        fn_text = ""

        # Get the href attribute of the first function link
        first_function_link = item['href']
        fn_name = first_function_link.split(".")[0]
        #if fn_name != "acos":
        #    continue

        first_function_url = url.rsplit('/', 1)[0] + '/' + first_function_link


        function_response = requests.get(first_function_url)
        function_soup = BeautifulSoup(function_response.content, 'html.parser')

        # get the type
        func_type = ""
        try:
            sum_1 = function_soup.find('div', {'id': 'title', 'class': 'title-content'})
            sum_2 = sum_1.find('h1', class_='title')
            sum_3 = sum_2.find('span', {'class':'subtitle'})
            func_type = sum_3.get_text(strip=True)
        except:
            func_type = "function type not found"

        fn_text += fn_name + " | "
        fn_text += func_type + " | "
        fn_text += first_function_url + " | "
        summary = function_soup.find('div', {'id': 'title', 'class': 'title-content'}).find('p', class_='summary')
        if summary:
            summary_text = summary.get_text(strip=False)
        else:
            summary_div = function_soup.find('div', {'id': 'content'})
            highest_level_p = summary_div.find(lambda tag: tag.name == 'p' and tag.parent == summary_div)
            if highest_level_p:
                summary_text = highest_level_p.get_text(strip=False)
            else:
                summary_text = "no summary found"


        summary_text = str(summary_text).replace("\n"," ")
        fn_text += summary_text + " | "


        usage_items = function_soup.find_all('div', {'class': 'usage item'})
        len_items = len(usage_items)
        examples = ""

        desc_found = False
        for n in range(len_items):
            usage_item = usage_items[n]

            fn = function_soup.find('code', {'class': 'vexsignature'})

            returntype = fn.find('span', {'class':'vexrtype'}).find('span').get_text(strip=True)

            examples +=  returntype + " "
            name = fn.find('span', {'class': 'vexname'}).get_text(strip=True)

            examples += name + "("
            args = fn.find_all('span', class_=lambda x: x in ['vexargtype', 'vexname'])
            args = args[1:]
            types = []
            typenames = []

            for arg in args:
                span_class = arg.get('class')[0]  # Get the first class name
                span_text = arg.get_text(strip=True)

                if span_class == 'vexargtype':
                    # Process as argtype
                    types.append(span_text)
                elif span_class == 'vexname':
                    # Process as name
                    typenames.append(span_text)


            for i in range(len(types)):
                examples += types[i] + " " + typenames[i]
                if i < (len(types)-1):
                    examples += ", "
            examples += ")"

            desc = usage_item.find('div', {"class": "content"})
            if desc:
                desc_text = desc.get_text(strip=False)
                desc_text = str(desc_text).replace("\n"," ")
                desc_text = desc_text[:-1][1:]
                examples += " [" + desc_text + "], "
                desc_found = True

            else:
                examples += ", "
        if desc_found:
            examples = examples
        else:

            summary = function_soup.find('div', {'id': 'content'})
            if not summary:
                alt_desc = "no desc found"
            else:
                highest_p = summary.find(lambda tag: tag.name == 'p' and tag.parent == summary)
                if not highest_p:
                    alt_desc = "no desc found"
                else:
                 alt_desc = highest_p.get_text(strip=False)

            alt_desc = str(alt_desc).replace("\n", " ")
            alt_desc = " [" + alt_desc + "], "
            examples = examples[:-2] + alt_desc

        fn_text += examples[:-2]
        fn_text = fn_text.replace("\t", " ")


    #except Exception as e:
    #    print(e)
    #    fn_text = fn_name + " | Error parsing url " + first_function_url

        # Extract the usage examples or relevant content
        # Modify the below line according to the specific structure of the function page
        #usage_examples = function_soup.find('section', {'id': 'examples'}).get_text(strip=True)

        #return usage_examples
        print(fn_text)
        descs.append(fn_text)
        with open(out_path, 'a', encoding="utf-8") as file:
            file.write(fn_text + "\n")
    print("End")
    return descs

# URL of the VEX functions index
vex_functions_url = 'https://www.sidefx.com/docs/houdini/vex/functions/index.html'

out_path = 'W:\\houdini-gpt\\used files\\vex-scraped.txt'
open(out_path, 'w').close()
# Get the usage examples for the first function
scraped = get_first_vex_function_usage(vex_functions_url, out_path)