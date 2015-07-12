HPOptim
=========================================
HPOptim is a Lua module that allows the user to interface with the Bayesian Optimization software package known as Spearmint via the Torch shell or within a Torch script. Before getting started, make sure that you have Spearmint setup properly [Spearmint](https://github.com/HIPS/Spearmint) as well as [Torch](https://github.com/torch). The goal of this project is to provide a convenient way for Torch users to perform hyper-parameter optimization using only Lua and the Torch framework.

#### Setup
**STEP 1: Clone HPOptim: ** 
1. git clone https://github.com/mechaman/HPOptim
**STEP 2: Create model.lua & config.json: ** 
0. The HPOptim folder must always exist in the same directory as
config.json and model.lua.
1. The config.json file is a list of the different hyper-parameters along with properties such as the type or range of values to try for each hyper-parameter.
2. The model.lua file must contain a function named trainHyper that takes a table as input and returns an error. The table is made up of key-value pairs where the keys are the names of the parameters you defined in config.json and the values are the suggested hyper-parameter values from Spearmint. Access these suggested values in model.lua to completely define your objective function or model. Samples of these files can be found in the sample directory.
3. After both these files are completed move into the HPOptim directory and run setup.sh.
4. Important: I have made it such that the input type for each parameter can only be FLOAT. In order for Spearmint to be most effective, it is suggested that the user project their input range to log10 space. When a hyper-parameter value has been suggested to model.lua, simply use: math.pow(10,hyperparameter) to map it back to its proper value. The following paper provides more information on this technique: 

	Input Warping for Bayesian Optimization of Non-stationary Functions  
	Jasper Snoek, Kevin Swersky, Richard Zemel and Ryan Prescott Adams  
	International Conference on Machine Learning, 2014 

**STEP 2:  ** 