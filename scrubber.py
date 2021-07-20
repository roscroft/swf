import re
scrubbed = []
desired_columns = [0,10,11,12,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33]
# All rank abbreviations, surrounded by spaces
rank_abbrev = re.compile(r"(?i)( |^)(PV1|PVT|PFC|SPC|CPL|SGT|SSG|SFC|MSG|1SG|SGM|CSM|WO1|WO2|WO3|WO4|WO5|W01|W02|W03|W04|W05|1LT|2LT|LT|CPT|MAJ|LTC|COL|BG|MG|LTG|GEN)( |^[a-z][A-Z]|$)")
# All ranks spelled out
rank = re.compile(r"(?i)( |^)(private( first class)?|specialist|corporal|(staff |master |first )?sergeant( first class| major)?|(first |second |1st |2nd )?lieutenant|captain|major|(lieutenant )?colonel)( |^[a-z][A-Z]|$)")
# Component
comp = re.compile(r"(?i)( |^)(NCO|NCOIC|OIC)( |^[a-z][A-Z]|$)")
# Pronouns
pronoun = re.compile(r"(?i)( |^)(he|she)( |^[a-z][A-Z]|$)")
possessive_pronoun = re.compile(r"(?i)( |^)(his|hers)( |^[a-z][A-Z]|$)")
nominative_pronoun = re.compile(r"(?i)( |^)(him|her)( |^[a-z][A-Z]|$)")

def replace(data_csv):
    with open(data_csv, "r+") as cohort:
        for line in cohort:
            #print(line)
            data = line.strip().split(",")
            if data != ['']:
                #print(data)
                write_line = []
                first_name_regex = f"(?i)( |^){data[3]}( |^[a-z][A-Z]|$)"
                last_name_regex = f"(?i)( |^){data[4]}( |^[a-z][A-Z]|$)"
                first_name = re.compile(first_name_regex)
                last_name = re.compile(last_name_regex)
                
                for i in range(len(data)):
                    if i in desired_columns:
                        c_str = data[i]
                        c_str = do_sub(first_name, c_str)
                        c_str = do_sub(last_name, c_str)
                        c_str = do_sub(rank_abbrev, c_str)
                        c_str = do_sub(rank, c_str)
                        c_str = do_sub(comp, c_str)
                        c_str = do_sub(pronoun, c_str, " they ")
                        c_str = do_sub(possessive_pronoun, c_str, " their ")
                        c_str = do_sub(nominative_pronoun, c_str, " their ")
                        write_line.append(c_str)
                scrubbed.append(",".join(write_line)+"\n")
    
    with open("C:/Users/adher/Documents/SWF/out_file.csv", "w+") as out_file:
        out_file.writelines(scrubbed)

def do_sub(regex, work_string, sub_text=" SM "):
    return re.sub(regex, sub_text, work_string)


if __name__ == "__main__":
    cohort_file = "C:/Users/adher/Documents/SWF/cohort2.csv"
    replace(cohort_file)