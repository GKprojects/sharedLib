def call(String envName) {
    def env = [:]
    switch (envName) {
        case 'devopsgreen':
            env.activeNamesapce = 'devopsgreen'
            env.clusters = [ 'stg' ]
            break
        case 'devopsdev':
            env.activeNamesapce = 'devopsdev'
            env.clusters = [ 'uat-1' ]
        case 'dev':
            env.activeNamespace = 'dev'
            env.clusters = ['dev']
            break
        case 'stg':
            env.activeNamespace = 'stg'
            env.clusters = ['stg']
            break
        case 'tst':
            env.activeNamespace = 'tst'
            env.clusters = ['tst']
            break
        case 'uat':
            env.activeNamespace = 'uat-blue'
            env.clusters = [ 'uat-1' , 'uat-2', 'uat-3' ] 
            break
        case 'altair':
            env.activeNamespace = 'altair'
            env.clusters = [ 'altair-1' , 'altair-2', 'altair-3' ] 
            break
        case 'draco':
            env.activeNamespace = 'draco'
            env.clusters = [ 'draco-1' , 'draco-2', 'draco-3' ] 
            break
        case 'eldar':
            env.activeNamespace = 'eldar-blue'
            env.clusters = [ 'eldar' ]
            break
        // Add more cases for other folders
        default:
            error("Unknown folder name: ${envName}")
    }
    return env
}
