#! python3
import sys
import pprint
import traceback
import os


###############################################################################################
### configure and input
###############################################################################################
filename =""
fo_main=""
fo_out=""
fo_sub=""
key_word = ["SocketTimeoutException", "SocketException"]
pp = pprint.PrettyPrinter(indent=4)
current_folder = os.path.dirname(os.path.abspath(__file__))
try:
    fo_main=""
    if len(sys.argv) == 2: ### input is file
        filename = sys.argv[1]
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
                    fo_out=open(current_folder + "\\" + pid_field+"_"+tid_field+".txt", 'w')
                    fo_out.write(log)
                    fo_out.close()
                    log=""
                    fo_sub.close()


            line_main = fo_main.readline()

        fo_main.close()
        print("Press ENTER to exit")
        input()
    elif len(sys.argv) > 2: ### input are multiple files
        for fn in sys.argv:
            if (fn==sys.argv[0]):
                continue
            fo_main=open(fn, 'r')
            line_main = fo_main.readline()
            pid_field = 0
            tid_field = 0
            while(line_main != ""):
                try:
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
                            fo_sub=open(fn,'r')
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
                            fo_out=open(current_folder + "\\" + pid_field+"_"+tid_field+".txt", 'a')
                            fo_out.write(log)
                            fo_out.close()
                            log=""
                            fo_sub.close()


                    line_main = fo_main.readline()
                except:
                    print("Unexpected error:", sys.exc_info()[0])
                    print("File in read:", fo_main.__str__())
                    traceback.print_exc(file=sys.stdout)
                    input()
                    break;

            fo_main.close()
except:
    print("Unexpected error:", sys.exc_info()[0])
    traceback.print_exc(file=sys.stdout)
    print("Press ENTER to exit")
    input()
