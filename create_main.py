from libs.createData import *
import sys

t_opt = get_opt(sys.argv[1:])
func = t_opt.get('func')
run(func)