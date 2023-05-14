import datetime
from dateutil import parser
import argparse

#aggregates the number of elements in a class
def aggr(fluid=set[list,tuple], cat=set[list,tuple], no_cls_agr=bool, len_cat=bool, set_datetime=bool) -> dict:

    # Variables and container
    res_cont={}
    currenttime = (datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
    current_date = parser.parse(currenttime)

    try:
        # Set date and time if to be included
        res_cont.update({"date_&_time":current_date}) if set_datetime == True else None

        # Class reference         
        [res_cont.update({str(ref):classed(fluid, ref, len_cat)}) for ref in cat]   
        res_cont.update({"unclassed":classed(fluid, cat, len_cat, flag = 1)}) if no_cls_agr == True else None
        return res_cont
    except:
        print("InputError: {} or {} unsupported input type".format(type(fluid),type(cat)))
        raise

#This function aggregates element present in the class
def classed(fluid, ref, len_cat, flag=0, res=0):
    for datum in fluid:
        i = (len(datum)) if len_cat == True else datum
        if flag==0 and i == ref: res+=1
        if flag==1 and i not in ref: res+=1
    return res

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--fluid',
        help='List of data to be categorized and aggregated',
        required=True,
        default=None)
    parser.add_argument(
        '--cat', 
        help='Reference of caetgorization', 
        required=True, 
        type=set[list,tuple,dict], 
        default=None)
    parser.add_argument(
        '--no_cls_agr',
        help='Width of frame to capture from camera.',
        required=False,
        type=bool,
        default=False)
    parser.add_argument(
        '--len_cat',
        help='Height of frame to capture from camera.',
        required=False,
        type=bool,
        default=False)
    parser.add_argument(
        '--set_datetime',
        help='Number of CPU threads to run the model.',
        required=False,
        type=bool,
        default=False)
    args = parser.parse_args()

    aggr(args.fluid, args.cat, args.no_cls_agr, args.len_cat,args.set_datetime)

if __name__ == '__main__':
  main()