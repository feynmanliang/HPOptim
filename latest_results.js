db = connect("localhost:27017/spearmint")
jobs = db['constant_timestep.jobs'].aggregate([
    { $project: {
        id: true,
        val_loss: "$values.main",
        _id: false
    }},
    { $sort: {
       id: -1
    }}
])

while ( jobs.hasNext() ) {
    printjson( jobs.next() )
}
