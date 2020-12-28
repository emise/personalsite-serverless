# Personal Site (serverless)

This is a serverless implementation of my personal website. It uses AWS Lambda functions to handle server-side work, and the ReactJS frontend is hosted in S3.


Content updates can be made via:

- uploading photos to the right bucket in S3
- adding text to the allWords.js file


## Development

Build package + watch for changes: `npm run dev`
Start Express server: `npm start`


To make changes to serverless functions, update `handler.py`. To create new endpoints, update the local `serverless.yml` file. API throttling is controlled from the yml file as well.

## Productionizing

Build package: `npm run build`

Upload the created `bundle.js` to the s3 bucket.
