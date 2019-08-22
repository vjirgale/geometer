import numpy as np


def is_multiple(a, b, axis=None, rtol=1.e-15, atol=1.e-8):
    """Returns a boolean array where two arrays are scalar multiples of each other along a given axis.

    This function compares the absolute value of the scalar product and the product of the norm of the arrays (along
    an axis). The Cauchy-Schwarz inequality guarantees in its border case that this equality holds if and only if one
    of the vectors is a scalar multiple of the other.

    For documentation of the tolerance parameters see :func:`numpy.isclose`.

    Parameters
    ----------
    a, b : array_like
        Input arrays to compare.
    axis : None or int
        The axis along which the two arrays are compared.
        The default axis=None will compare the whole arrays and return only a single boolean value.
    rtol : float, optional
        The relative tolerance parameter.
    atol : float, optional
        The absolute tolerance parameter.

    Returns
    -------
    numpy.ndarray or bool
        Returns a boolean array of where along the given axis the arrays are a scalar multiple of each other (within the
        given tolerance). If no axis is given, returns a single boolean value.

    """
    a = np.asarray(a)
    b = np.asarray(b)

    if axis is None:
        a = a.ravel()
        b = b.ravel()

    ab = np.sum(a * b.conj(), axis=axis)
    return np.isclose(ab*ab.conj(), np.sum(a*a.conj(), axis=axis)*np.sum(b*b.conj(), axis=axis), rtol, atol)


def hat_matrix(*args):
    r"""Builds a skew symmetric matrix with the given scalars in the positions shown below.

    .. math::

        \begin{pmatrix}
            0  &  c & -b\\
            -c &  0 & a \\
            b  & -a & 0
        \end{pmatrix}

    Parameters
    ----------
    a, b, c : float
        The scalars to use in the matrix.

    Returns
    -------
    numpy.ndarray
        The resulting antisymmetric matrix.

    """
    if len(args) == 1:
        x = np.array(args[0])
    else:
        x = np.array(args)

    n = int(1+np.sqrt(1+8*len(x)))//2

    if n == 3:
        a, b, c = x
        return np.array([[0, c, -b],
                         [-c, 0, a],
                         [b, -a, 0]])

    result = np.zeros((n, n), x.dtype)
    i, j = np.triu_indices(n, 1)
    i, j = i[::-1], j[::-1]
    result[j, i] = -x
    result[i, j] = x

    return result


def null_space(A):
    """Constructs an orthonormal basis for the null space of a A using SVD.

    Parameters
    ----------
    A : array_like
        The input matrix.

    Returns
    -------
    numpy.ndarray
        Orthonormal basis for the null space of A (as column vectors in the returned matrix).

    """
    u, s, vh = np.linalg.svd(A, full_matrices=True)
    cond = np.finfo(s.dtype).eps * max(vh.shape)
    tol = np.amax(s) * cond
    dim = np.sum(s > tol, dtype=int)
    Q = vh[dim:, :].T.conj()
    return Q
