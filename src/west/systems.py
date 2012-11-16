from __future__ import division; __metaclass__ = type

import logging
log = logging.getLogger(__name__)
import westpa

import numpy
from west.binning import NopMapper
        
class WESTSystem:
    '''A description of the system being simulated, including the dimensionality and
    data type of the progress coordinate, the number of progress coordinate entries
    expected from each segment, and binning. To construct a simulation, the user must
    subclass WESTSystem and set several instance variables.
    
    At a minimum, the user must subclass ``WESTSystem`` and override
    :method:`initialize` to set the data type and dimensionality of progress
    coordinate data and define a bin mapper.
    
    :ivar pcoord_ndim:    The number of dimensions in the progress coordinate.
                          Defaults to 1 (i.e. a one-dimensional progress 
                          coordinate).
    :ivar pcoord_dtype:   The data type of the progress coordinate, which must be
                          callable (e.g. ``numpy.float32`` and ``long`` will work,
                          but ``'<f4'`` and ``'<i8'`` will not).  Defaults to
                          ``numpy.float64``.
    :ivar pcoord_len:     The length of the progress coordinate time series
                          generated by each segment, including *both* the initial
                          and final values.  Defaults to 2 (i.e. only the initial
                          and final progress coordinate values for a segment are
                          returned from propagation).
    :ivar bin_mapper:     A bin mapper describing the progress coordinate space.
    :ivar bin_target_counts: A vector of target counts, one per bin.
    '''
    
    def __init__(self, rc=None):
        self.rc = rc or westpa.rc
        
        # Number of dimentions in progress coordinate data
        self.pcoord_ndim = 1
        
        # Length of progress coordinate data for each segment
        self.pcoord_len = 2
        
        # Data type of progress coordinate
        self.pcoord_dtype = numpy.float32
        
        # Mapper
        self.bin_mapper = NopMapper()
        self._bin_target_counts = None
        
        self.bin_target_counts = [1]
        
    @property
    def bin_target_counts(self):
        return self._bin_target_counts
    
    @bin_target_counts.setter
    def bin_target_counts(self, target_counts):
        maxcount = max(target_counts)
        self._bin_target_counts = numpy.array(target_counts, dtype=numpy.min_scalar_type(maxcount))
                
    def initialize(self):
        '''Prepare this system object for use in simulation or analysis,
        creating a bin space, setting replicas per bin, and so on. This
        function is called whenever a WEST tool creates an instance of the
        system driver. 
        '''
        pass
            
    def prepare_run(self):
        '''Prepare this system for use in a simulation run. Called by w_run in
        all worker processes.'''
        pass
    
    def finalize_run(self):
        '''A hook for system-specific processing for the end of a simulation run
        (as defined by such things as maximum wallclock time, rather than perhaps
        more scientifically-significant definitions of "the end of a simulation run")'''
        pass

    def new_pcoord_array(self, pcoord_len=None):
        '''Return an appropriately-sized and -typed pcoord array for a timepoint, segment,
        or number of segments. If ``pcoord_len`` is not specified (or None), then 
        a length appropriate for a segment is returned.'''
        
        if pcoord_len is None:
            pcoord_len = self.pcoord_len
        return numpy.zeros((pcoord_len, self.pcoord_ndim), self.pcoord_dtype)

    
    def new_region_set(self):
        raise NotImplementedError('This method has been removed.')
