#! python3
import pprint

filename="log_sample.txt"
pp = pprint.PrettyPrinter(indent=4)

fo=open(filename,'r')
line = fo.readline()
pid_field = 0
tid_field = 0
while(line != ""):
    field_array = line.split(" ")
    date_field = field_array[1]
    time_field = field_array[2]
    pid_field = field_array[3]
    tid_field = field_array[4]
    tag_field = field_array[5]
    msg_field = field_array[6]
    if (msg_field.find("SocketTimeoutException") != -1 or msg_field.find("SocketException") != -1):
        break;
    line = fo.readline()
fo.close()
fo=open(filename,'r')
line = fo.readline()
while(line != ""):
    field_array = line.split(" ")
    if (pid_field == field_array[3] and tid_field == field_array[4]):
        pp.pprint(line)
    line = fo.readline()

print("Press ENTER to exit")
input()
