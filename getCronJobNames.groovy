def call(String jobName) {
    if (jobName.contains('KF4')) {
        return [ 'accountsv2', 'auditlogv2', 'auditv2-cleanup', 'auditv2', 'automationv2-deletion', 
        'automationv2-mail', 'automationv2', 'batchuserv2', 'gcmv2', 'indexmanagerv2', 'schedulerv2'
         ]
    } else if (jobName.contains('KF3')) {
        return [ 'audit-cleanup', 'audit', 'automation', 'scheduler' ]
    } else {
        return [ 'test' ]
    }
}

