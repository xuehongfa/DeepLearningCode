import angr
import simuvex
import claripy
#from angr import Project, SimProcedure
from angrutils import plot_cfg
import archinfo
from angrutils.exploration import NormalizedSteps
import os
function_list=[]
with open("/home/hongfa/workspace/bzip2_ML/function_list.txt",'r') as f:
    functions_list = f.read().splitlines()


def analyze(b, addr, function,name=None):
    start_state = b.factory.blank_state(addr=addr,add_options=angr.options.unicorn)
    
    start_state.stack_push(0x0)

    cfg = b.analyses.CFGAccurate(fail_fast=True, starts=[addr], initial_state=start_state, context_sensitivity_level=1,keep_state=True, call_depth=50, normalize=True)
    nodes = cfg.get_all_nodes(addr)
    #cfg = b.analyses.vfg.VFG(fail_fast=True, starts=[addr], initial_state=start_state, context_sensitivity_level=1)
#cfg = b.analyses.CFG(fail_fast=True,  resolve_indirect_jumps=False,collect_data_reference=False, force_complete_scan=False)
    #cfg= b.analyses.CFGFast(keep_state=True)
    #plot_cfg(cfg, "%s_cfg" % (name), asminst=True, vexinst=False, debug_info=False, remove_imports=False,
    #        remove_path_terminator=False)

    #start_state = b.factory.blank_state(addr=addr,add_options={
    #                                                            simuvex.o.CONSERVATIVE_READ_STRATEGY} | simuvex.o.resilience_options)
    start_state.options.add(angr.options.FAST_MEMORY)
    start_state.options.add(angr.options.FAST_REGISTERS)
    start_state.stack_push(0x0)

    pg = b.factory.simgr(start_state)
    #pg.use_technique(angr.exploration_techniques.veritesting.Veritesting())
    #pg.use_technique(angr.exploration_techniques.DFS())
    pg.use_technique(NormalizedSteps(cfg))
    #pg.use_technique(angr.exploration_techniques.explorer.Explorer(cfg=cfg))
    unique_states = set()

    def check_loops(path):
        last = path.bbl_addrs[-1]
        c = 0
        for p in path.bbl_addrs:
            if p == last:
                c += 1
        return c > 1

    def step_func(lpg):
        #lpg.stash(filter_func=check_loops, from_stash='active', to_stash='looping')
        lpg.stash(filter_func=lambda path: path.addr == 0, from_stash='active', to_stash='found')
        #print lpg
        return lpg

    pg.step(step_func=step_func, until=lambda lpg: len(lpg.active) == 0, n=100)
    subfolder = '/home/hongfa/workspace/bzip2_ML/train/' + str(function) + '/'
    os.mkdir(subfolder)
    i = 0
    for stash in pg.stashes:


        #subfolder = '/home/hongfa/Dropbox/openssl/openssl_path/' + str(function) + '/'
        #os.mkdir(subfolder)
        for p in pg.stashes[stash]:
            #print p

            filename = 'trace_' + str(i)
            #subfolder='/home/hongfa/Dropbox/openssl/openssl_path/'+str(function)+'/'
            #os.mkdir(subfolder)
            with open(subfolder + filename, 'w') as f:
                for addr in p.history.bbl_addrs:


                    f.write(format(addr,'#04x')+'\n')
            i+=1
    #entry_fun=cfg.kb.functions[hex(addr)]
    #nodes = entry_fun.block_addrs

    for n in nodes:
        #print n
        filename = 'trace_' + str(i)
        with open(subfolder + filename, 'w') as f:

            f.write(format(n.addr, '#04x') + '\n')
        i+=1

	    
#            plot_cfg(cfg, "%s_cfg_%s_%d" % (name, stash, c), path=p, asminst=True, vexinst=False, debug_info=False,
#                     remove_imports=True, remove_path_terminator=True)
            #c += 1


if __name__ == "__main__":

    #proj = angr.Project("/usr/local/ssl/bin/openssl", load_options={'auto_load_libs': False})
    proj = angr.Project("/home/hongfa/workspace/bzip2_ML/bzip2.ml", load_options={'auto_load_libs': False})
    #cfg = proj.analyses.CFG(fail_fast=True)
    #proj.hook()
    print len(function_list)
    for j in range(0,len(function_list)):
        i=function_list[j]
        #print entry_fun.addr
        #proj.hook(entry_fun.addr)
        #entry_fun = getFuncAddress("BZ2_hbAssignCodes")
        entry_fun = proj.loader.main_object.get_symbol(i)

        #print hex(fun).rstrip("L")
        #print hex(entry_fun)
        if entry_fun:
            #en = cfg.kb.functions[entry_fun.addr]
            #blocks = en.block_addrs

            proj.hook(entry_fun.addr)
            print i
            analyze(proj, entry_fun.addr, function=i,name=str(i))
