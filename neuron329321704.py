'''
Defines a class, Neuron329321704, of neurons from Allen Brain Institute's model 329321704

A demo is available by running:

    python -i mosinit.py
'''
class Neuron329321704:
    def __init__(self, name="Neuron329321704", x=0, y=0, z=0):
        '''Instantiate Neuron329321704.
        
        Parameters:
            x, y, z -- position offset
            
        Note: if name is not specified, Neuron329321704_instance is used instead
        '''
        
        # load the morphology
        from load_swc import load_swc
        load_swc('Scnn1a-Tg3-Cre_Ai14_IVSCC_-170426.03.01.01_328933585_m.swc', self,
                 use_axon=False, xshift=x, yshift=y, zshift=z)

        # custom axon (works because dropping axon during import)
        from neuron import h
        self.axon = [h.Section(cell=self, name='axon[0]'),
                     h.Section(cell=self, name='axon[1]')]
        for sec in self.axon:
            sec.L = 30
            sec.diam = 1
            sec.nseg = 1
        self.axon[0].connect(self.soma[0](0.5))
        self.axon[1].connect(self.axon[0](1))
        self.all += self.axon
        
        self._name = name
        self._insert_mechanisms()
        self._discretize_model()
        self._set_mechanism_parameters()
    
    def __str__(self):
        if self._name is not None:
            return self._name
        else:
            return "Neuron329321704_instance"
                
    def _insert_mechanisms(self):
        from neuron import h
        for sec in self.all:
            sec.insert("pas")
        for mech in [u'CaDynamics', u'Ca_HVA', u'Ca_LVA', u'Ih', u'Im', u'K_P', u'K_T', u'Kv3_1', u'NaTs', u'Nap', u'SK']:
            self.soma[0].insert(mech)
    
    def _set_mechanism_parameters(self):
        from neuron import h
        for sec in self.all:
            sec.Ra = 58.48
            sec.e_pas = -81.3347930908
        for sec in self.apic:
            sec.cm = 1.91
            sec.g_pas = 0.000470085432332
        for sec in self.axon:
            sec.cm = 1.0
            sec.g_pas = 0.000697267815518
        for sec in self.dend:
            sec.cm = 1.91
            sec.g_pas = 0.000170092914249
        for sec in self.soma:
            sec.cm = 1.0
            sec.ena = 53.0
            sec.ek = -107.0
            sec.gbar_Im = 0.00117797
            sec.gbar_Ih = 0.000558439
            sec.gbar_NaTs = 0.482482
            sec.gbar_Nap = 0.000433224
            sec.gbar_K_P = 0.007372
            sec.gbar_K_T = 0.000187833
            sec.gbar_SK = 0.00025635
            sec.gbar_Kv3_1 = 0.138371
            sec.gbar_Ca_HVA = 0.00046307
            sec.gbar_Ca_LVA = 0.00897297
            sec.gamma_CaDynamics = 0.000884733
            sec.decay_CaDynamics = 764.194
            sec.g_pas = 0.000125114
    
    def _discretize_model(self):
        for sec in self.all:
            sec.nseg = 1 + 2 * int(sec.L / 40)

