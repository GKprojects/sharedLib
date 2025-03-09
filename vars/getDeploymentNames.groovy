def call(String jobName) {
    if (jobName.contains('KF4')) {
        return [ 'accountsv2', 'adminv2', 'analyticssyncv2', 'analyticsv2', 'apidocsv2', 
            'appstorev2', 'appstoreworkerv2', 'appsv2', 'asyncworkerv2', 'auditlogv2', 
            'auditlogworkerv2', 'auditv2', 'auditworkerv2', 'batchuserv2', 'botv2', 
            'casereportv2', 'casev2', 'caseworkerv2', 'changestreamv2', 'chatv2', 
            'chatworkerv2', 'commentv2', 'commonv2', 'communityv2', 'connectorv2', 
            'datasetv2', 'datasetworkerv2', 'digitalhubv2', 'documentparserv2', 
            'eventsubscriptionv2', 'eventworkerv2', 'externalobjectv2', 'filetransferworkerv2', 
            'flowv2', 'flowworkerv2', 'formreportv2', 'formv2', 'formworkerv2', 'gcmv2', 
            'gcmworkerv2', 'governancev2', 'integrationv2', 'integrationworkerv2', 'lowcodev2', 'licensev2',
            'marketplacev2', 'metadatav2', 'notificationv2', 'notificationworkerv2', 'portalv2', 
            'postv2', 'processinternalv2', 'processreportv2', 'processreportworkerv2', 'processv2', 
            'projectreportv2', 'projectv2', 'projectworkerv2', 'route', 'schedulerv2', 'searchv2', 
            'searchworkerv2', 'teamv2', 'traceworkerv2', 'uploadv2', 'uploadworkerv2', 'userv2', 'workflowworkerv2'
         ]
    } else if (jobName.contains('KF3')) {
        return [ 'accounts', 'admin', 'apidocs', 'audit', 'auditworker', 'batchuser', 'channel', 
                  'client', 'comment', 'common', 'dataset', 'datasetworker', 'eventworker', 'flow', 
                  'integration', 'main-client', 'marketplace', 'notification', 'notificationworker', 
                  'process', 'project', 'report','scheduler', 'search', 'searchworker', 'stream', 'upload', 'user'
        ]
    } else {
        return [ 'test' ]
    }
}
