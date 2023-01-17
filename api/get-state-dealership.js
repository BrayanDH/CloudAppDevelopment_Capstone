const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

params = {
  COUCH_URL: process.env.COUCH_URL,
  IAM_API_KEY: process.env.IAM_API_KEY,
  COUCH_USERNAME: process.env.COUCH_USERNAME,
  DBNAME: process.env.BBDD2,
  state: 'Texas',
};

async function main(params) {
  const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY });
  const cloudant = CloudantV1.newInstance({
    authenticator: authenticator,
  });
  cloudant.setServiceUrl(params.COUCH_URL);
  selector = { state: 'Texas' };
  try {
    let records = await cloudant.postFind({ db: params.DBNAME, selector: selector });
    //console.table(modifiedRecords);
    return { result: records.result.docs };
  } catch (error) {
    return { error: error.description };
  }
}
