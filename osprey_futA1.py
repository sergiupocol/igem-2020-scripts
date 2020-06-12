import osprey

# initializing osprey
osprey.start()

strand = osprey.Strand('2pt1.pdb')

# On strand we will define both the sequence and conformation space
# On every residue for which setLibraryRotamers is not called
# it will be modelled as fixed in space with its position found in the
# pdb file supplied.

# This is where Alanine scanning comes in.
# We can take the top K (tbd) most important residues and
# if they are close enough* to the ligand, i.e. we consider
# it to be on the surface of the protein, we can set it's possible
# mutations to negatively charged polar residues.

# negatively charged residues: ASP, GLUE
# polar uncharged: SER, THR, ASN, GLN, TYR, CYS


# Conversely, "deep" residues should only mutate to hydrophobic

# Fow now here are the residues in the "native pocket"
# For chain X residue number N, the residue is identified by 'XN'
strand.flexibility['A54'].setLibraryRotamers(osprey.WILD_TYPE, 'ASP', 'GLU') # Wild type means the residue is free to be unchanged
# BUT will still have it's flexibility modelled
strand.flexibility['A55'].setLibraryRotamers(osprey.WILD_TYPE, 'ASP', 'GLU')
strand.flexibility['A145'].setLibraryRotamers(osprey.WILD_TYPE, 'ASP', 'GLU')
strand.flexibility['A185'].setLibraryRotamers(osprey.WILD_TYPE, 'ASP', 'GLU')
strand.flexibility['A239'].setLibraryRotamers(osprey.WILD_TYPE, 'ASP', 'GLU')
strand.flexibility['A241'].setLibraryRotamers(osprey.WILD_TYPE, 'ASP', 'GLU')
strand.flexibility['A242'].setLibraryRotamers(osprey.WILD_TYPE, 'ASP', 'GLU')
strand.flexibility['A241'].setLibraryRotamers(osprey.WILD_TYPE, 'ASP', 'GLU')
# Now the conf space is defined
confSpace = osprey.ConfSpace(strand)

# DEFAULT CONFIG FOR NOW
ffparams = osprey.ForceFieldParams()
ecalc = osprey.EnergyCalculator(confSpace, ffparams)
confEcalc = osprey.ConfEnergyCalculator(confSpace, ecalc)
emat = osprey.EnergyMatrix(confEcalc)
astar = osprey.AStarMPLP(emat, confSpace)


# find the best sequence and rotamers
gmec = osprey.GMECFinder(confSpace, astar, ecalc).find()
