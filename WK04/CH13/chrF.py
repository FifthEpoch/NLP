import numpy as np
import math

def compute_chfF(_ref, _hyp, _beta=2, _k=2):
    """
    :param _ref: reference string (human translation)
    :param _hyp: hypothesis string (machine translation)
    :return: a real value chrF
    """
    # process both _ref and _hyp so that there is no space
    ref = _ref.replace(" ", "")
    hyp = _hyp.replace(" ", "")

    chrP = 0.0
    chrR = 0.0
    for n in range(_k):

        # collecting data for chrP for n-gram
        matched_n_gram_chrP = 0
        num_n_gram_chrP = len(hyp) - n
        ref_matched = np.ones(len(ref) - n)
        for i in range(num_n_gram_chrP):
            matched = 0
            for j in range(len(ref) - n):
                if ref[j:j+n+1] == hyp[i:i+n+1] and ref_matched[j]:
                    ref_matched[j] = 0
                    matched = 1
                    break
            matched_n_gram_chrP += matched

        print(f'{n+1}-gram chrP:        {matched_n_gram_chrP} / {num_n_gram_chrP} = {matched_n_gram_chrP / num_n_gram_chrP}')
        chrP += matched_n_gram_chrP / num_n_gram_chrP

        # collecting data for chrR for n-gram
        matched_n_gram_chrR = 0
        num_n_gram_chrR = len(ref) - n
        hyp_matched = np.ones(len(hyp) - n)
        for i in range(num_n_gram_chrR):
            matched = 0
            for j in range(len(hyp) - n) :
                if hyp[j:j+n+1] == ref[i:i+n+1] and hyp_matched[j]:
                    hyp_matched[j] = 0
                    matched = 1
                    break
            matched_n_gram_chrR += matched

        print(f'{n+1}-gram chrR:        {matched_n_gram_chrR} / {num_n_gram_chrR} = {matched_n_gram_chrR / num_n_gram_chrR}')
        chrR += matched_n_gram_chrR / num_n_gram_chrR

    # get the average of the two scores for all the n-grams
    chrP /= _k
    chrR /= _k

    return ((1 + (_beta**2)) * chrP * chrR) / (((_beta**2) * chrP) + chrR)

def print_res(_ref, _hyp, _chrF):
    print(f'reference:  {_ref}')
    print(f'hypothesis: {_hyp}')
    print(f'chrF:       {_chrF} = {round(_chrF, 2)}\n')

reference = "witness for the past,"
hypothesis_01 = "witness of the past,"
hypothesis_02 = "past witness"

chrF = compute_chfF(reference, hypothesis_01)
print_res(reference, hypothesis_01, chrF)
chrF = compute_chfF(reference, hypothesis_02)
print_res(reference, hypothesis_02, chrF)