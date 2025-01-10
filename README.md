Sync on Linux:
`cp -R --exclude='README*' --exclude='.Trashes' --exclude='.fseventsd' --exclude='.metadata_never_index' --exclude='.Spotlight-V100' ~/git/co2sensor/* /Volumes/CIRCUITPY/`

Sync on macOS:
`cp -R ~/git/co2sensor/* /Volumes/CIRCUITPY/ 2>/dev/null`


What are safe levels of CO and CO2 in rooms?
See: https://www.kane.co.uk/knowledge-centre/what-are-safe-levels-of-co-and-co2-in-rooms
	
250-400ppm 	Normal background concentration in outdoor ambient air
400-1,000ppm 	Concentrations typical of occupied indoor spaces with good air exchange
1,000-2,000ppm 	Complaints of drowsiness and poor air.
2,000-5,000 ppm 	Headaches, sleepiness and stagnant, stale, stuffy air. Poor concentration, loss of attention, increased heart rate and slight nausea may also be present.
5,000 	Workplace exposure limit (as 8-hour TWA) in most jurisdictions.
>40,000 ppm 	Exposure may lead to serious oxygen deprivation resulting in permanent brain damage, coma, even death.
