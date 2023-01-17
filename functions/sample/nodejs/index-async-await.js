const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');
require('dotenv').config();

/**
 * Get all dealerships
 */

params = {
  COUCH_URL: process.env.COUCH_URL,
  IAM_API_KEY: process.env.IAM_API_KEY,
  COUCH_USERNAME: process.env.COUCH_USERNAME,
  DBNAME: process.env.BBDD2,
  state: 'Texas',
};

// async function main(params) {
//   const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY });
//   const cloudant = CloudantV1.newInstance({
//     authenticator: authenticator,
//   });
//   cloudant.setServiceUrl(params.COUCH_URL);
//   try {
//     let dbList = await cloudant.getAllDbs();
//     console.log(dbList);
//     let records = await cloudant.postAllDocs({ db: params.DBNAME, includeDocs: true, limit: 10 });
//     console.log(records);
//     return { result: result.result.rows };
//   } catch (error) {
//     return { error: error.description };
//   }
// }

// function getAllRecords(cloudant, DBNAME) {
//   return new Promise((resolve, reject) => {
//     cloudant
//       .postAllDocs({ db: DBNAME, includeDocs: true, limit: 10 })
//       .then((result) => {
//         resolve({ result: result.result.rows });
//       })
//       .catch((err) => {
//         console.log(err);
//         reject({ err: err });
//       });
//   });
// }

async function main(params) {
  const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY });
  const cloudant = CloudantV1.newInstance({
    authenticator: authenticator,
  });
  cloudant.setServiceUrl(params.COUCH_URL);
  try {
    let records = await cloudant.postAllDocs({ db: params.DBNAME, includeDocs: true, limit: 10 });
    const modifiedRecords = records.result.rows.map((row) => row.doc);
    //console.table(modifiedRecords);
    return modifiedRecords;
  } catch (error) {
    return { error: error.description };
  }
}

//main(params);

async function main2(params) {
  const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY });
  const cloudant = CloudantV1.newInstance({
    authenticator: authenticator,
  });
  cloudant.setServiceUrl(params.COUCH_URL);
  selector = { state: 'Texas' };
  try {
    let records = await cloudant.postFind({ db: params.DBNAME, selector: selector });
    console.table(records);
    return { result: records.result.docs };
  } catch (error) {
    return { error: error.description };
  }
}

main2(params);
