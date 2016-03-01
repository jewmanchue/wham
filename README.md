### WHAM-GRAPHENING [![Build Status](https://travis-ci.org/zeeev/wham.svg?branch=master)](https://travis-ci.org/zeeev/wham) [![Code Climate](https://codeclimate.com/github/zeeev/wham/badges/gpa.svg)](https://codeclimate.com/github/zeeev/wham)


WHAM-GRAPHENING has increased accuracy for deletions, duplications and inversions.

The genotyping module can be slow in high-copy regions.  I recommend filtering SVs prior to genotyping (-k skips genotyping).

Full documentation is coming soon. 

Workflow:

![alt tag](https://github.com/zeeev/wham/blob/master/docs/wg.png)

======

### WHAM [![Build Status](https://travis-ci.org/zeeev/wham.svg?branch=master)](https://travis-ci.org/zeeev/wham)

All WHAM documents can be found on the wiki:

http://zeeev.github.io/wham/

WHole-genome Alignment Metrics (WHAM) is a structural variant (SV) caller that integrates several sources of mapping information to identify SVs.  WHAM classifies SVs using a flexible and extendable machine-learning algorithm (random forest).  WHAM is not only accurate at identifying SVs, but its association test can identify shared SVs enriched in a cohort of diseased individuals compared to a background of healthy individuals.   

WHAM can be easily run as a stand alone tool or as part of gkno (http://gkno.me) or bcbio-nextgen (http://bcbio-nextgen.readthedocs.org) pipelines.  

Currently we are preparing the WHAM manuscript.  If you would like to use and cite this tool, for the time being, please cite the WHAM github page.



