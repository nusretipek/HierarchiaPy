import numpy as np


def dci(self) -> float:

    """Directional consistency index (DCI)

    Returns
    -------
    dc_index : float
        Directional consistency index (DCI) of the given interaction matrix (rounded to 4 decimal places)

    Notes
    -----
    It is the proportion of occurrences of a behaviour from high frequency to low frequency (H -> L) for all
    pairs in a group. It is averaged out using (H-L)/(H+L)=DCI. The domain is 0 to 1 meaning no directional asymmetry to
    complete unidirectional respectively.

    References
    ----------
    * Van Hooff JARAM, Wensing JAB. 1987. Dominance and its behavioural measures in a captive wolf pack. In: Frank HW,
    editor. Man and Wolf. Dordrecht, Olanda (Netherlands): Junk Publishers pp.219-252.
    """
    
    # Calculate DCI
    mat = self.mat.astype('float64')
    np.fill_diagonal(mat, np.nan)
    dc_index = round(np.nansum(np.abs(mat - np.transpose(mat))) / 2 / np.nansum(mat), 4)
    
    # Return statement
    return dc_index
