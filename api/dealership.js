const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');
require('dotenv').config();

params = {
  COUCH_URL: process.env.COUCH_URL,
  IAM_API_KEY: process.env.IAM_API_KEY,
  COUCH_USERNAME: process.env.COUCH_USERNAME,
  DBNAME: process.env.BBDD2,
  state: 'Texas',
};

console.log(params);

async function main(params) {
  const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY });
  const cloudant = CloudantV1.newInstance({
    authenticator: authenticator,
  });
  cloudant.setServiceUrl(params.COUCH_URL);
  try {
    let records = await cloudant.postAllDocs({ db: params.DBNAME, includeDocs: true, limit: 10 });
    const modifiedRecords = records.result.rows.map((row) => {
      return {
        doc: {
          ...row.doc,
        },
      };
    });
    return { data: modifiedRecords };
  } catch (error) {
    return { error: error.description };
  }
}
