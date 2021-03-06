import angr
import simuvex
import claripy
#from angr import Project, SimProcedure
from angrutils import plot_cfg
import archinfo
from angrutils.exploration import NormalizedSteps


def analyze(b, addr, name=None):
    start_state = b.factory.blank_state(addr=addr)
    start_state.stack_push(0x0)

    cfg = b.analyses.CFGAccurate(fail_fast=True, starts=[addr], initial_state=start_state, context_sensitivity_level=5,
                                 keep_state=True, call_depth=100, normalize=True)

    #plot_cfg(cfg, "%s_cfg" % (name), asminst=True, vexinst=False, debug_info=False, remove_imports=False,
    #        remove_path_terminator=False)

    start_state = b.factory.blank_state(addr=addr,add_options={
                                                                simuvex.o.CONSERVATIVE_READ_STRATEGY} | simuvex.o.resilience_options)

    #start_state = b.factory.blank_state(addr=addr, add_options=angr.options.unicorn)
    start_state.stack_push(0x0)

    pg = b.factory.path_group(start_state)
    pg.use_technique(NormalizedSteps(cfg))

    unique_states = set()

    def check_loops(path):
        last = path.addr_trace[-1]
        c = 0
        for p in path.addr_trace:
            if p == last:
                c += 1
        return c > 1

    def step_func(lpg):
        #lpg.stash(filter_func=check_loops, from_stash='active', to_stash='looping')
        lpg.stash(filter_func=lambda path: path.addr == 0, from_stash='active', to_stash='found')
        print lpg
        return lpg

    pg.step(step_func=step_func, until=lambda lpg: len(lpg.active) == 0, n=100)

    for stash in pg.stashes:
        c = 0
        i = 0
        for p in pg.stashes[stash]:
            #print p

            filename = 'trace_' + str(i)
            with open('/home/hongfa/workspace/bzip2_binary/train/3/' + filename, 'w') as f:
                for addr in p.addr_trace:


                    f.write(format(addr,'#04x')+'\n')
            i+=1
            plot_cfg(cfg, "%s_cfg_%s_%d" % (name, stash, c), path=p, asminst=True, vexinst=False, debug_info=False,
                     remove_imports=True, remove_path_terminator=True)
            #c += 1
def getFuncAddress( funcName, plt=None ):
    found = [
        addr for addr,func in cfg.kb.functions.iteritems()
        if funcName == func.name and (plt is None or func.is_plt == plt)
        ]
    if len( found ) > 0:
        print "Found "+funcName+"'s address at "+hex(found[0])+"!"
        return found[0]
    else:
        raise Exception("No address found for function : "+funcName)

if __name__ == "__main__":
    #proj = angr.Project("/usr/local/ssl/bin/openssl", load_options={'auto_load_libs': False})
    proj = angr.Project("/home/hongfa/workspace/bzip2.x86", load_options={'auto_load_libs': False})
    cfg = proj.analyses.CFGFast(fail_fast=True)
    #proj.hook()
    #entry_fun = proj.loader.main_bin.get_symbol("addFlagsFromEnvVar")
    #print entry_fun.addr
    #proj.hook(entry_fun.addr)
    entry_fun = getFuncAddress("BZ2_hbAssignCodes")
    proj.hook(entry_fun)
    #print hex(fun).rstrip("L")
    print hex(entry_fun)
    analyze(proj, entry_fun, "BZ2_hbAssignCodes")
