import re

def parse_data(configurations_list,read_log):
    output = {}
    output_status = False
    for item in configurations_list:
        print('ITEM')
        print(item)
        command = item['command_name']
        case_name = item['case_name']
        pattern_to_match = item['regex_str']
        threshold_value = item['threshold_value']
        type_of_value = item['type_of_value']
        range = item['t_range']
        negate = item['negate']
        # status =item.status
        symptoms = item['symptoms']
        resolutions = item['resolution']

        if negate == True:
            continue

        if type_of_value == 'String':
            regex_to_parse = str(command) + r'([\s\S]+?)' + str(pattern_to_match)  + str(threshold_value)
            if re.search(regex_to_parse, read_log, re.IGNORECASE):
                output_status = True
                output[case_name] = {}
                if threshold_value!='':
                    output[case_name]['value'] = threshold_value
                output[case_name]['symptoms'] = symptoms
                output[case_name]['resolutions'] = resolutions

                if re.search('(sh|show) log', str(command)):
                    regex_error_log = str(command) + r'([\s\S]+?)('+ str(pattern_to_match) + r'[\s\S]*?)\.'
                    error_log = re.search(regex_error_log,read_log, re.IGNORECASE)
                    error_log=error_log.group(2)
                    print(error_log)
                    output[case_name]['error_log'] = error_log

                else:
                    regex_error_log = str(command) + r'([\s\S]+?)(' + str(pattern_to_match) + str(threshold_value) + ')'
                    error_log = re.search(regex_error_log, read_log, re.IGNORECASE)
                    error_log = error_log.group(2)
                    print(error_log)
                    output[case_name]['error_log'] = error_log


        elif type_of_value == 'integer':
            regex_to_parse = str(command) + r'([\s\S]+?)' + str(pattern_to_match)
            if re.search(regex_to_parse, read_log):
                temp_value = re.search(regex_to_parse, read_log, re.IGNORECASE)
                temp_value = temp_value.group(2)
                temp_value = int(temp_value)
                print(temp_value)

                if range == '>':
                    if temp_value > int(threshold_value):
                        output_status = True
                        output[case_name] = {}
                        output[case_name]['value'] = threshold_value
                        output[case_name]['symptoms'] = symptoms
                        resolutions = re.sub('xx', str(threshold_value), resolutions)
                        resolutions = re.sub('yy',str(temp_value), resolutions)
                        output[case_name]['resolutions'] = resolutions

                        regex_error_log = str(command) + r'([\s\S]+?)(' + str(pattern_to_match) + ')'
                        error_log = re.search(regex_error_log, read_log, re.IGNORECASE)
                        error_log = error_log.group(2)
                        print(error_log)
                        output[case_name]['error_log'] = error_log

                elif range == '<':
                    if temp_value < int(threshold_value):
                        output_status = True
                        output[case_name] = {}
                        output[case_name]['value'] = threshold_value
                        output[case_name]['symptoms'] = symptoms
                        resolutions = re.sub('xx', str(threshold_value), resolutions)
                        resolutions = re.sub('yy',str(temp_value), resolutions)
                        output[case_name]['resolutions'] = resolutions

                        regex_error_log = str(command) + r'([\s\S]+?)(' + str(pattern_to_match) + ')'
                        error_log = re.search(regex_error_log, read_log, re.IGNORECASE)
                        error_log = error_log.group(2)
                        print(error_log)
                        output[case_name]['error_log'] = error_log

    return output_status,output
