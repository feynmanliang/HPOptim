require 'torch'
require 'nn'

----------------------- Test Architecture --------------------------------

-----------------------------------------
function getTableFromTensor(teData, nInputs, nOutputs)

    local train_X = teData[1] -- take the first two columns as X
    local train_y = teData[2] -- take the last column as y

   local tableData = {}
   function tableData:size() return train_X[1]:size(1) end

   for i=1, 100 do
     tableData[i] = { train_X:narrow(1,i,1), train_y:narrow(1,i,1) }
   end

   return tableData
end
-----------------------------------------

-- Usage HPOptim Module
local HPOptim = require('/HPOptim/HPOptim.lua') -- load HPOptim module
HPOptim.init()
HPOptim.findHP(60 * 60 * 8) -- Spearmint runs for 30 seconds
