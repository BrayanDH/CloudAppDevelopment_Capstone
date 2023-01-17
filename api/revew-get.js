const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

params = {
  COUCH_URL: COUCH_URL,
  IAM_API_KEY: IAM_API_KEY,
  COUCH_USERNAME: COUCH_USERNAME,
  BBDD1: BBDD1,
  BBDD2: BBDD2,
  dealerId: 13,
};

async function main(params) {
  const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY });
  const cloudant = CloudantV1.newInstance({
    authenticator: authenticator,
  });
  cloudant.setServiceUrl(params.COUCH_URL);
  let dealer = [];
  let reviews = [];
  try {
    //Get dealer data from BBDD2
    dealerId = parseInt(params.dealerId);
    const dealerData = await cloudant.postFind({ db: params.BBDD2, selector: { id: dealerId } });
    dealer = dealerData.result.docs;
    //Get reviews data from BBDD1
    const reviewsData = await cloudant.postFind({ db: params.BBDD1, selector: { dealership: dealerId } });
    reviews = reviewsData.result.docs;
    return { dealer, reviews };
  } catch (error) {
    return { error: error.description };
  }
}

main(params);
