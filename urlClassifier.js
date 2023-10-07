function urlType(url) {
        // YouTube video URL pattern
        const youtubePattern = /^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+/;
        // File URL pattern, looking for URLs ending with file extension
        const filePattern = /[^/\\&\?]+\.\w{3,4}(?=([\?&].*$|$))/;

        if (youtubePattern.test(url)) {
            return Promise.resolve({type: 'youtube'});
        } else if (filePattern.test(url)) {
            let extension = url.match(filePattern)[0].split('.').pop();
            return Promise.resolve({type: 'file', fileType: extension});
        } else {
            // Attempting to access the url to check if it's a valid website.
            return axios.get(url).then(response => {
                if(response.status === 200) {
                    return {type: 'website'};
                } else {
                    return {type: 'unknown'};
                }
            }).catch(error => {
                return {type: 'unknown'};
            });
        }
    }

window.urlType = urlType;
