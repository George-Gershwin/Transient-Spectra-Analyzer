from qt_task import Task
from multiprocessing import Process


class TaskFit(Task):
    def __init__(self, fw, parent=None):
        super(TaskFit, self).__init__(parent)
        self.fw = fw  # fit widget

    def preRun(self):
        self.fw.set_btns_enabled(False)  # disable buttons
        self.fw.fitter.is_interruption_requested = self.isInterruptionRequested  # setup a function

    def run(self):
        print('Fitting...')
        self.run_fit()

    def run_fit(self):
        # hard model fit
        if self.fw.current_model.connectivity.count(0) == 0:
            if self.fw.current_model.method is 'RFA':
                self.fw.fitter.obj_func_fit()
            elif self.fw.current_model.method is 'femto':
                self.fw.D_fit = self.fw.fitter.var_pro_femto()
            else:
                self.fw.fitter.var_pro()

        elif self.fw.current_model.connectivity.count(0) == int(self.fw.sbN.value()):  # pure MCR fit
            self.fw.fitter.HS_MCR_fit(c_model=None)
        else:  # mix of two, HS-fit
            self.fw.fitter.HS_MCR_fit(c_model=self.fw.current_model)

    def postRun(self):  # after run has finished
        if self.fw.fitter.c_model is not None:
            self.fw.current_model = self.fw.fitter.c_model

        self.fw.update_fields_H_fit()

        self.fw._C = self.fw.fitter.C_opt
        self.fw._ST = self.fw.fitter.ST_opt

        self.fw.plot_opt_matrices()
        self.fw.print_stats()

        self.fw.set_btns_enabled(True)  # enable buttons
