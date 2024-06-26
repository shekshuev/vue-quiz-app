module.exports = {
    publicPath: process.env.NODE_ENV === "production" ? "/static/" : "/",
    css: {
        loaderOptions: {
            sass: {
                additionalData: `@import "@/styles/_variables.scss";`
            }
        }
    }
};
