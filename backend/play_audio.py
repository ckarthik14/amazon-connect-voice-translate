import base64
from pydub import AudioSegment
from pydub.playback import play
import io

# Your base64 encoded string
base64_audio = "SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4Ljc2LjEwMAAAAAAAAAAAAAAA//NgxAAeu9ngAUkYAQQJMIwTAGAMNvI21BQKGLns5////ru78R3d3d3dEKIgAIR3dz/R3f0RPRP93EIiIiIgGLc//+IXX//////+u7n/1z/6iJ7noBgYGBu57oiIiITgAAif/+7u7gYAAIXELQq4GBi3dEREL0d3+J1EQv/4iJ7uAAAgR+AeHjEJhICwkDFGCSwAF0lmwsRTET3L//NixBQlUkZdvZygAHxqadMXum5TmChYeDJRo9JuXPmEAJwygCxINvgDNyLiUwQIgtIE48qubiDBeCK+eJ9ZNk+Tji9+ZuXGNA2YyDaBjgyPVdsXAOQeDey+nDV4NjINzxAYkFf/+nX+pa//7rY3Tt+5sXR2F8zOlb//4q/8od/8gc5PCwoAws/EJyUPhuoCBqqqqqqmoAAZAAZwOf/zYsQOI4I6fZWbaAAGctyAkymnMAHjXhcFchhqMLUJiLCmynAHEgOBy7paQd5JnBgBScKuJgiUSIimPxKEciFhWfZAwTWVD4YGBeE4MU1FIY5dG9Q3hajAuHQvw72GKalPF0niCBfzLGsUyTEWv/0P9v8/z237MyB00t+mgaqMf+j+z9Q9P/Ej/+N/kAANPB6m3GEA8to9RbSkk9//82LEECRiQqm/mXgAEBfVyNuxQabKggt+W4UKf+HJ0FMNcIInYDXC5TsEzxqgvdu0LhMmNQ6XvFcV2ilAN9hnly8xuBeGh6F/W4dm+f/6i1n/+rbVismz///9Z390/96wojPHu/Q9zQzyR8Vv///9SY+v///0ZeO8o/yPf/s/FR/9X/lf9gcxdYWOCyUCetJKeVCaLCEsyESjLdnm//NgxA4jGjq0AZh4AH3SgiRWBRdGAhGKs33IaylR55EgPtZjQyoiJBXJR9BVEVNxnKAfSrHepyXHqM9IQYCnLxDUWKLVk7KyKZ4fKFuKyiYynTpgQFKYW1JGHbVieVne7jN7dJZn0qIK1Zb13nV9FRFat1eZv6f///V55bb1///eTHiP/////////VVAiBms/lamdodwp69W+yF5//NixBAhiiKpZ9iIAKGstnYy8YztplbVNbLnNpY0dHeCdHPNTQpBkALqTMmCZGTC4oLYvOoxICN5FlolEkX1mo9cyPjZR1DnDtU+OQI3Kz5HlptJM8+WR8JKrLAvzfWdKqb9Teavu5qzaBvqRMQxXZ///+Q7vR8pJBRjQm0VGUPVOPSqwAAPRVZJTMFwTgWODsZkNMFqXjOLnKklT//zYsQZIFuesZaLzl//RuoHPq4gzlVqx/DeGNNbfDVDmN2FZhdM4TLKjUUjR1ZSydx0/c5OaPAOJea3NNfHRsSKsjjxL0fottEO1Y4l5rTZytzlQ1rEv///////Ps0qfKvTmPP/spyPVEFQCpmFPyFftn7vvhWgKQAgnsP3L38RPI2FJEKkcIQRQJx39Zu7mTMv7mvu9cuRqDBGBW7/82LEJx6b5pR20gtIUm6es2Wx//OLPmssbG4o73FCSG5yf4gWquSj1myhAC6fCf/OJD+QhiN35A6pMQEx3irrQjf/////////+b1TQluknp9TeY6IrkB0a6NQjCOWgAMqQhbAmgsCX8t6gkGyj4MOYTiSKAbTPH0i0+f76rArTVVbp+nCCAgWGr853bJBnzDFvPHWmOIuHLEw+Djq//NgxDwes06ltsvKXBEI9TkK2c6eRrTiDNvnJRs5ziIqqv0f/9UDrNOMX///////////mOp3QoqYzjAdO1PU+hTw8ATI4/L1vicmQoS8FpZRNfrepsgarbCaHKNCEIC6rmHXlGKTPoR6eT4fbHfy19Zacso94vaMGIiqWVcWxqni+t/H7/fkFCrwaJn+oMbxtXPotZBgGgm7amn///NixFAfaha1lsZQljqc2NFR5uoqeEZ/LK/7n/83NS0H1/BgmOA/UGf4f//++IAeJLSGkf+tsp85nGVlGnUpVUre9W8IFoDWWI+jvFOFzBaTZB9hovkrl4aK3uuJUDPj/GmKa3XYPAPS5Z2A0HkTTxAT/4Jo9QTcg78Mboi6FN5PS3l6sGFKk7e3kV+5fZPl1Rp/2U7syMl5GsfO/v/zYsRiHrvewjZ5hUOEo3/6JaifkJo0/9Ceh50qdc4gSfwwqc9GYgwSgwsnYjUmkAnBdWXEnGqKVL5dLiyKo0akqOdZ10VpKZSSKksyR4Vy+GFmMQhP/idRGBQCRuxV/3+Ff/NwLOAHGHjzThBYGgeQHBweC5RoPn3Ifz8Chlf2QD4//EMF5wASX/////7TlPRMhKd5Lut3qT9E//7/82LEdx/T5rY+iFFUb+63QypuGEqqASjkcdcFh1AUOjB5akMzTZejsWys0yEJp/M8v/NcyPXMdUfiLLLUv7+60v96bT7gXtGHB2ij4tSlmc8r/vYd82ME9/+WJA3Aa3t4SbRBSv4RDzZPFHKSDg8GoKAvIGcCAbYpkC5XArWHGOH/uWQLTwaKDEQWJDgeYIUJlqmYdl0skLkwBklJ//NgxIcefBa6VChRHGKFlWMGsaQ7TeWOG93ZEwuxLEs1LY+Zqr6HvuWsU84sOvxJgqshJfin8RSppfT8kY2GTX//9v/8uH/nUOfnyp/9b8//rfq4IkpVqKUowSg4c/wbKXUMTG2EgLAMwIHVTqMcWJEeeLkB4MFQqiwIZ4QImWeYhltimAf93MCiTpEn2cn6YclOzK2p0WJ0tZWx//NixJwfPAq3GgJGFdHkIycsNqdWwrTnUplX8ihaZRbdtE61ZWGPOZ9FKnFjP/1Z2qWQz/lv9P0frV6ZWxgti3eoqXrsbRkfkEnby0VUCQCjlLKWVypRBEdqodDrOpRIWGkFhqS1CjkzIMyQ/udr08r6YiuKyeCIm7hBCi0oswhGPuRbyHw21X/K1SqykWwEZQKs7/9WyqanqVkM/v/zYsSvHdwOqxwwytm7f/t1L//R+FerG+pWmrzvOS3/+tZKZbmkiVVrs5u1VOjP8yaokk/5pHNOJPLTLb+/7ORznabjPM9zQVHyAQnMVIELIDe48L6KxjXblEmWBYeCkIRCAWBsHQC1io4WOJNG0ULXTXLXO10zV2Sa0qt7NytV//XHytQ6rK181y3w1//x/+sXwzSzf7f/XKr/qsX/82LExx4EBn5SGI3J/x+v/8f/K97fP7N/Os//G1/DX+1rV//9ztTWqrBQsowGrIs9agJAAAJEIFMltPEuocgWl8r2E+wV5P7RDX0n0tct8jNLmjSteY5XpeQ3Rj1GtLou40mpyp2cUg7QcAmJPUt3HlJjYw2tJEQWIqevWptZ8xtXr3JfuV5QuDouJPZY96LXLudJnjSU2NjGpYqZ//NgxN8c29JMNUJAAP2dv6mGjGvVDds72xdNf5mplTXqWl1+et1uV6fvcNXtYxi80VMNt4dWunXhDcOUs7Ajh26a7u1VwrWPrSv9Vqa9un/edPS6w5RX9TF6H1qOA4jc2buILAhhpjO43MSaRPJjnjrD5Z3m9ZZU1qx2vcpq3JyzSX86TVy/UsdzuZ42b2N6JvNO5UfWbyCG2h2J//NixPpBZBYc7Y/AAPae78Hw9SvPFn1bekzSKxW9XoshUa3W5I2/5fQYrChHYQ2a44C6YBL0OO8skZfLI3CFjutSS2G2H2Ef0hFb23dOdciG6SAQQBjI8ncFSN3Kn0lGqkykoys5pjsTlWxar25fnbbMwdnEMM7cCDIxYy1/Ld6k3GM/98ZI3J9Ys81LKGhyv6LDms7WqK78/q9X5f/zYsSEO2Pmsl+YwAI238gaZl01EYvNSZ34gyzmfb2/3lreqkDc79Tu8s8d95Z3YjF69Ur1am+fnjlyQVbtzmVuaxq/9XVWlyyoef+873///vnKmGerH9w/P6TmHd61zD+9uZZ2cceY67a1+9Y8vc1r+9+/uJKqhAcGSo4/cdokeCwJfGQtwBsJuvAI4HBJ1DACAtgsVtaeyHoel0P/82DEJiYqDpFv2XgADZn+Vr1Fo5Qq1rU6rZo1mB6+jZeO61yq1c0WQ5GIShRPTkHYLYh7gsHgwzR1hoV7ArELJ/BiTyU+dXx8a+Pnd7/O/jPy8gVw9rTfxXL6L547Jus//8TU5kMlqHnyoiYVzvl5UNfXsKkwD0c9Rp//0uFgJYAfYf0X8rywh02lNXfU4HjNFWYWaYJrWrxbAkL/82LEHCDaQpWGw8S8oYuTcLbNvDexVrCVJpR9L7tx9cx4PzbXq9Z3jjTS4T5oqEt46yTUqr1I3PrnOYOIJdzTapH3/yVQxVKIV0MjbN2aDBGfRDo0K5Wf1dkf/wp1rP+g5PLcW2UQKGse2pwvqqfBWj/0wopEOhDa1rdR8TKkULbdx7AGKb6QMbMWzDkKtMndBS7K1sGhnQ9PyYWp//NixCgkGxaJhtMK2NOxyVfEZu1iooXSxlVvcf0ZXqEaBCfBYBUfQhA+MgAQawCYYg4OArB4UjoeDoawNzMyjhIRMhvoKi7ujAgqLCr9ImomMILo69TGVOnpuzaF//+ZiTvRHbv/9ipHAyvdo/2us/YKkUBhlZKVCpGv/KqNQq1I6nWqaW3EyxLFfm5ePwVETMrGzGdIzKsSVl4Xn//zYsQnHeoKmO7CRr6wtGo1vhbO3sULEDRUmZNkroIUTxAhNCkUxdKWf7FS8/ln0+CQ6Cmq/AKkZkwaN/sJUWFHPdEVKv8oRQtcV+sgCYLxeuP32bmpPWb/WaKiYRIbFdn+psgELqzFmGA0GCZbGyr+DrZRi5EnvNzWcbH3piP8+g9ntPXPTNmazzUzkfTNHq84fPNwGR80TFZ7YuD/82DEPx8bNoRGywS8gl4RjkRw9NaSx0zLlb2q35goUv3KyI5So2iHkdZP9W///9SUM1pv/+o0KgFOrYox4I1P+dcE3WV01oVU0zUFhKWPnbAyYPxv/OlgIWLfZ1mViNJl973G+3ElkQUnb0j3aR58Na3VJvtSczcyYd1you8ElhwbVjV1w9p8XAjL2bPp1fq/ZZtDctpH08GRoa3/82LEUR0TGnROysS88KVzKi0L6Od1Zn//+rfr3//mJFgylEvIf/S+qxyZYlEY0iMVWH+bE3GhGoc6jHm5OMoFDs0mSXpjXkgMNFtWkkUis2LZls/uO+Scl6babf9hL/2EgqUwScAsOC4ThZRcLT2+rLVs5+a0dZ0HyBpJ/3HSYkjw2X6lC6c01v1+a3uab/Z0U1G253S7LZjxwucy//NixGwfuxZcLMmOnJQc86Cw1P0BZKnnSNxWhammVTIcxewwQziDjFL8eRKUms3FExpI2GeTrROvOaUmidaNNaqmm/WHVvVYtYYmJmDiSB44PgEQLBAAMA0GgjCsX1HXfX3+vf9FDRwsILjm/i1JQCs6Gf//LN9UekJCoZCRoKGoFInneEgdCtAVMhMzgIRCwFYKGgbAVUxBTUUzLv/zYsR9HZneIAB5kHQxMDBVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVUxBTUUzLjEwMFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVX/82DEcAAAA0gAAAAAVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVMQU1FMy4xMDBVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVX/82LEbwAAA0gAAAAAVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVTEFNRTMuMTAwVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//NixG8AAANIAAAAAFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVUxBTUUzLjEwMFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVf/zYsRvAAADSAAAAABVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVUxBTUUzLjEwMFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVX/82DEcAAAA0gAAAAAVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVMQU1FMy4xMDBVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVX/82LEbwAAA0gAAAAAVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVTEFNRTMuMTAwVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//NixG8AAANIAAAAAFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVTEFNRTMuMTAwVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVf/zYMRwAAADSAAAAABVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVUxBTUUzLjEwMFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVf/zYsRvAAADSAAAAABVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVMQU1FMy4xMDBVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVX/82LEbwAAA0gAAAAAVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVTEFNRTMuMTAwVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//NixG8AAANIAAAAAFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVXABCcRQ/EAey8YmxYWfC0tXHpaIgsH88XrF8HbE+xC1V9Y2tRnh2hJVyk3LZ4/G4tCzyizjTiIcICCbd6QPOChgWQPKNWhHe1bLT5ANDdQ+4+4+443BWzK5Sbm6h+l6fX43H6bnfMzv0vMDKlWYHaf/zYMRwAAADSAAAAAASmSAT1+MIZ0YlooD+W1lmWlpkTRuMw8J5gvYbl5UofpebLVRsaH6y/WdRqkSOJ5aZD6MyOWD9x50+QB/LZ4/1qvrG1qM8XsQtKVauKzq5afFkjj+WD9x+J51BNywfrL03JnNtWzryhQFYXFEjgwIEoGMNAEzOZzJUKOVJIyeiQUcjEYpBQ/EAAMJBYtaJAP/zYsT/NeQVhDJhmUjUAf1uyFa5JbEDEtrKwPHkPsLDAhlEdwkNB4Cg7TKF619ZtnDtXzh28YIaNYdph3OC+fHlCQBB+ReJv5r9ERKRIFDEpFTSuXdyDPtJuaeJuhdhxguMESXPIFLm/5eGp3PLcse8enFaTFPln+8Iru8RvaI4wwhb/4FLm/qNIr+b7tPf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0RoXVIr8FWeyxwCcUkrCAhQutZEiiK30vRDFW4M4YQrW6rv/484jUWEwmWXFIyThA8vv///ZtLOjv/yFI8wRgv/zYsTqHro+fFbRiwy4C/9Dn//89DCHVv9ewQUaoCjhQhjHE2gnEqMd9f/6hYiDBY+HCP/kZWogACUBMZiS7QSeHzgZbZppIGGVP4qDsvS/MJWFgXKloMCly09EpWWqLpX8pTHuUMXUFiteG6Wlxia5qbRs2hZh+i3UkU6KqssarDFDXUxGyhZv5qjopILJg9B6DkSBgv+Ofohz/8r/82LE/yYTemBE2kUwGm0EkcUHwPxgiPk/7f/9UV0ISP/zpyGnDxeXQdQjR0eTYshBxZKEv/x9Ds5+Sl2jHf/L1YTTZRkEAKOdrMA0LMpQTLTQ62uMlCTHAICkptjuX8WXcSuQ0ZIrsEBaZko7/7+C29j7fRnGW0lI70ulQoAsdEizTlHJJS1WzcCy7hyHpqsSc/P/+wtciowWDqxW//NixPYmS55YVtpPKLh/1v6Fv/o7aGDCiDlYrv8hn///v//5lKpQRYkYz0bRyoKEuX//UuoC2GPDKYMFZfkBEmYtsAgSfw75l4ZGgTEY5AhYHJjsmGKREYRDBh0BFYClLMUfUPoRPsNZyqHv7vRGZqUchq3AtRNE+PKOEtMwc05sB6jyZf6oaTtfxO1+q8juCmEguJgXKbTR+rF2ov/zYMTsIuOyRALaBTIhvo/tTlVkMhvm+NGvq/6azU1/lnPYzDUKAzcfVBzRiCQef/+T/iSiI4sNKgYBWWK8Mxvg6/Vjb40MRCFJgwKJDEAhEg6tYEAsBBFtYi1l+YjIaFyRi5YkRIwkDAJKrJbOaaCo/tRxJc+iiW9DWTUrf0l6h0rcweEQBBTSy6iuhjGblaURM6tlas2Z8rfR9f/zYsTvIsumMAziCxQrPK32R80ztmTVnqIuUpRIWVDTVKURHCTIYyt/1LVkqxl8ok5A8DMrhqqgVEV1DBkVCEgPsykhISxdScJpJpw3P/5Sutzf///5Rq55uayiIRo4jYeRky1HIyZZHL8mWyzllqfzJmscuWSyyykUv/LZkZNZKRkasDqORkyhgVT1YKCBOhjChUQhBEpB9XTK0Sn/82LE8yQrphAA4YrQ/ExH/ParExMTEzH+pRI0h4mJR7VpiSiRCEhaXEsNGQ/2sPSsrKLByDwZTEFNRTMuMTAwVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//NgxPIjBBWICkjRdFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV"

# Decode the base64 string
audio_data = base64.b64decode(base64_audio)

# Convert binary data to audio using pydub
audio = AudioSegment.from_file(io.BytesIO(audio_data), format="mp3")

# Play the audio
play(audio)
