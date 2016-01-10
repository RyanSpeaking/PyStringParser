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

## {{{ http://code.activestate.com/recipes/410692/ (r8)
# This class provides the functionality we want. You only need to look at
# this if you want to know how this works. It only needs to be defined
# once, no need to muck around with its internals.
class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False

try:
    fo_main=""
    if len(sys.argv) == 2: ### input is file
        print("single file")
        filename = sys.argv[1]
        fo_main=open(filename,'r')
        line_main = fo_main.readline()
        pid_field = ""
        pid_field_list = []
        tid_field = ""
        tid_field_list = []
        #while(line_main != ""):
        if line_main != "":
            ###############################################################################################
            ### find a line and parse for needed fields char by char
            ### fields for sample log: 1.DATE 2.TIME 3.PID 4.TID 5.LOG
            ###############################################################################################
            #field_array = line_main.split(" ")
            field_array = list(line_main)
            next_one = 1
            char_found = False
            space_found = False
            for c in field_array:
                if (c != ' '):
                    if (char_found == False and space_found == True):
                        next_one += 1
                    char_found = True
                    space_found = False
                    print(c + ", next_one=" + str(next_one))
                    for case in switch(next_one):
                        if case(1):
                            break
                        if case(2):
                            break
                        if case(3):
                            pid_field_list.append(c)
                            print("current pid_field_list=" + ''.join(pid_field_list))
                            break
                        if case(4):
                            tid_field_list.append(c)
                            print("current tid_field_list=" + ''.join(tid_field_list))
                            break
                    continue
                else:
                    char_found = False
                    space_found = True
                    continue
            pid_field = ''.join(pid_field_list)
            tid_field = ''.join(tid_field_list)

            for x in key_word:
                ###############################################################################################
                ### found
                ###############################################################################################
                if (line_main.find(x) != -1):
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
        print("multiple file")
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
    print("Press ENTER oh!!!")
    input()
    os.path.ismount("fddgredf`")
