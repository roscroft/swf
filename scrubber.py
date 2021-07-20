import re
scrubbed = []
desired_columns = [0,10,11,12,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33]
# All rank abbreviations, surrounded by spaces
sub_dict = {}
sub_dict["rank abbrev"] = ("PV1|PVT|PFC|SPC|CPL|SGT|SSG|SFC|MSG|1SG|SGM|CSM|Chief|Mr.|Mrs.|Ms.|WO1|WO2|WO3|WO4|WO5|W01|W02|W03|W04|W05|CW1|CW2|CW3|CW4|CW5|1LT|2LT|LT|CPT|MAJ|LTC|COL|BG|MG|LTG|GEN", "SM")
sub_dict["rank"] = ("private( first class)?|specialist|corporal|(staff |master |first )?sergeant( first class| major)?|(first |second |1st |2nd )?lieutenant|captain|major|(lieutenant )?colonel", "SM")
#sub_dict["comp"] = ("NCO|NCOIC|OIC", " SM ")
# Manually found nicknames
sub_dict["nicknames"] = ("Nick|Greg|Ozzy|Viera|Vic|Jon|Brandon|Alex|Louie|Rich|Bill", "SM")
sub_dict["possessive pronoun"] = ("his|hers", "their")
sub_dict["nominative pronoun"] = ("him|her", "them")
sub_dict["they"] = ("he|she", "they")
sub_dict["is"] = ("they is", "they are")
sub_dict["was"] = ("they was", "they were")
sub_dict["has"] = ("they has", "they have")
sub_dict["'s'"] = ("they's", "they're")

def regex_generator(match):
    # Regex breakdown:
    # (?i) - ignore case
    # \b - word boundary. Ensures {match} is matched only when a full word, proceeded and followed by non-word characters (a-z, 0-9, _)
    # ({match}) - f-string, for match described above
    return re.compile(fr"(?i)\b({match})\b")

for key, value in sub_dict.items():
    sub_dict[key] = (regex_generator(value[0]), value[1])

def replace(data_csv, out_file):
    with open(data_csv, "r+") as cohort:
        for line in cohort:
            data = line.strip().split(",")
            write_line = []
            names = [regex_generator(name) for name in data[3].split(" ") + data[4].split(" ") if name != ""]
            for i in range(len(data)):
                if i in desired_columns:
                    c_str = data[i]
                    for name in names:
                        c_str = re.sub(name, "SM", c_str)
                    for _, (pattern, sub_string) in sub_dict.items():
                        c_str = re.sub(pattern, sub_string, c_str)
                    # Remove multiple occurences of "SM"
                    c_str = re.sub(r"SM( SM)+", "SM", c_str)
                    write_line.append(c_str)
            scrubbed.append(",".join(write_line)+"\n")
    
    with open(out_file, "w+") as out_file:
        out_file.writelines(scrubbed)

if __name__ == "__main__":
    cohort_file = "./cohort2.csv"
    out_file = "./out_file.csv"
    replace(cohort_file, out_file)