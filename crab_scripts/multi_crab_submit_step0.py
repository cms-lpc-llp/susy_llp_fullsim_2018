if __name__ == '__main__':

    from CRABAPI.RawCommand import crabCommand
    from CRABClient.ClientExceptions import ClientException
    from httplib import HTTPException

    #from CRABClient.UserUtilities import config
    #config = config()
    from WMCore.Configuration import Configuration
    config = Configuration()

    config.section_("General")
    config.General.workArea = 'crab'
    config.General.transferOutputs = True
    config.General.transferLogs = True

    config.section_("JobType")
    config.JobType.pluginName = 'PrivateMC'

    config.section_("Data")
    config.Data.inputDBS = 'global'
    config.Data.splitting = 'EventBased'
    config.Data.unitsPerJob = 500
    config.Data.totalUnits = 100000
    config.Data.publication = True

    config.section_("Site")
    config.Site.storageSite = 'T2_US_Caltech'
    # We want to put all the CRAB project directories from the tasks we submit here into one common directory.
    # That's why we need to set this parameter (here or above in the configuration file, it does not matter, we will not overwrite it).

    def submit(config):
        try:
            crabCommand('submit', config = config)
        except HTTPException as hte:
            print "Failed submitting task: %s" % (hte.headers)
        except ClientException as cle:
            print "Failed submitting task: %s" % (cle)

    #############################################################################################
    ## From now on that's what users should modify: this is the a-la-CRAB2 configuration part. ##
    #############################################################################################
    ev = 100000 #100k events
    mchi_list = [200]
    pl_list = [1000]
    mode_list = ["n3n2-n1-hbb-hbb"]
    pset_dir = "/afs/cern.ch/user/j/jmao/work/public/releases/cms-llp/CMSSW_10_2_11/src/"
    for i in range(len(mode_list)):
	mode = mode_list[i]
	for mchi in mchi_list:
	    for pl in pl_list:
		spec = mode+"_mh{}_pl{}_ev{}".format(mchi,pl,ev)
		
    		config.General.requestName = 'CMSSW_10_2_11_'+mode+"_mchi{}_pl{}_ev{}".format(mchi,pl,ev)+'_GENSIM_CaltechT2'
		config.Data.outputPrimaryDataset = spec
		config.Data.outLFNDirBase = '/store/group/phys_exotica/jmao/aodsim/RunIIAutumn18/GENSIM/MSSM-1d-prod/'
		if "x1n2" in mode:
			config.Data.outLFNDirBase = '/store/group/phys_exotica/jmao/aodsim/RunIIAutumn18/GENSIM/MSSM-2d-prod/'
		config.JobType.psetName = pset_dir + "crab_scripts/Fullsim_step0_cfg.py"
		#config.JobType.psetName = pset_dir + "Fullsim_TChiHH_prompt_mChi"+str(mchi)+"_step0_cfg.py"
		config.JobType.numCores = 8
		print 'config %s' %(config.JobType.psetName)
		print 'output %s' %(config.Data.outLFNDirBase)
		print 'output %s' %(config.Data.outputPrimaryDataset)
		submit(config)
