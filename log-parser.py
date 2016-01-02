#! python3
import sys
import pprint


###############################################################################################
### configure and input
###############################################################################################
key_word = ["SocketTimeoutException", "SocketException"]
try:
    pp = pprint.PrettyPrinter(indent=4)
    filename = sys.argv[1]
except:
    print("Unexpected error:", sys.exc_info()[0])
    filename="log_sample.txt"

fo_main=open(filename,'r')
line_main = fo_main.readline()
pid_field = 0
tid_field = 0
while(line_main != ""):
    ###############################################################################################
    ### find a line
    ###############################################################################################
    field_array = line_main.split(" ")
    pid_field = field_array[2]
    tid_field = field_array[4]
    tag_field = field_array[5]
    msg_field = field_array[6]
    for x in key_word:
        ###############################################################################################
        ### found
        ###############################################################################################
        if (msg_field.find(x) != -1):
            ###############################################################################################
            ### find all the logs of the found thread
            ###############################################################################################
            log=""
            fo_sub=open(filename,'r')
            line_sub = fo_sub.readline()
            while(line_sub != ""):
                field_array = line_sub.split(" ")
                if (pid_field == field_array[2] and tid_field == field_array[4]):
                    pp.pprint(line_sub)
                    log+=line_sub
                line_sub = fo_sub.readline()
            ###############################################################################################
            ### print to file
            ###############################################################################################
            fo_out=open(filename+"_"+pid_field+"_"+tid_field+".txt", 'w')
            fo_out.write(log)
            fo_out.close()
            log=""
            fo_sub.close()


    line_main = fo_main.readline()

fo_main.close()
print("Press ENTER to exit")
input()
