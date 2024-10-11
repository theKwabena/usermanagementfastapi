import Cookies from 'js-cookie'
const cookiesStorage = {
    setItem: function(key, state) {
      // console.log(state)
      return Cookies.set('data', state, { expires: 3 });
    },
    getItem: function(key) {
      return Cookies.get()
    }
  };


  export {cookiesStorage}