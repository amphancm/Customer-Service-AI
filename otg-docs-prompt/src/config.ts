// export const ENV = {
//     development: {
//       API_BASE_URL: "http://192.168.122.120:5500",
//     },
//     staging: {
//       API_BASE_URL: "http://localhost:5500",
//     },
//     production: {
//       API_BASE_URL: "http://localhost:5500",
//     },
//   };
  
//   // Detect environment
//   export const CONFIG =
//     process.env.NODE_ENV === "production"
//       ? ENV.production
//       : process.env.NODE_ENV === "staging"
//       ? ENV.staging
//       : ENV.development;

// export const ENV = {
//   development: {
//     API_BASE_URL: "http://192.168.122.120:5500",
//   },
//   staging: {
//     API_BASE_URL: "http://localhost:5500",
//   },
//   production: {
//     API_BASE_URL: "http://localhost:5500",
//   },
// };

// // Detect environment
// export const CONFIG =
//   process.env.NODE_ENV === "production"
//     ? ENV.production
//     : process.env.NODE_ENV === "staging"
//     ? ENV.staging
//     : ENV.development;

export const ENV = {
  development: {
    API_BASE_URL: import.meta.env.VITE_API_BASE_URL,
  },
  staging: {
    API_BASE_URL: "http://localhost:5500",
  },
  production: {
    API_BASE_URL: "http://localhost:5500",
  },
};

// Detect environment
export const CONFIG =
  process.env.NODE_ENV === "production"
    ? ENV.production
    : process.env.NODE_ENV === "staging"
    ? ENV.staging
    : ENV.development;