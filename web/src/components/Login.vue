<template>
  <div>
    <button @click="handleClickSignIn" v-if="!isSignIn" :disabled="!isInit">sign in</button>
    <button @click="handleClickSignOut" v-if="isSignIn" :disabled="!isInit">sign out</button>
    <div v-if="isSignIn">
      <span>{{user.name}}</span>
      <img :src="user.img">
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data () {
    return {
      isInit: false,
      isSignIn: false,
      error: '',
      user: {
        name: '',
        //img: '',
        email: ''
      }
    }
  },

  methods: {
    handleClickSignIn(){
      this.$gAuth.signIn()
      .then(user => {
        // On success do something, refer to https://developers.google.com/api-client-library/javascript/reference/referencedocs#googleusergetid
        this.isSignIn = this.$gAuth.isAuthorized
        if(this.isSignIn){
          let profile = user.getBasicProfile()
          this.user.name = profile.getName()
          //this.user.img = profile.getImageUrl()
          this.user.email = profile.getEmail()

          localStorage.username = this.user.name
          //localStorage.userimg = this.user.img
          localStorage.useremail = this.user.email
        }
      })
      .catch(error  => {
        // On fail do something
        this.error = error
      })
    },

    handleClickSignOut(){
      this.$gAuth.signOut()
      .then(() => {
        // On success do something
        this.isSignIn = this.$gAuth.isAuthorized
        localStorage.removeItem('username')
        localStorage.removeItem('useremail')
        //localStorage.removeItem('userimg')
      })
      .catch(error  => {
        // On fail do something
        this.error = error
      })
    }
  },
  mounted(){
    if (localStorage.username) {
      this.user.name = localStorage.username
    }
    //if (localStorage.userimg) {
    //  this.user.img = localStorage.userimg
    //}
    if(localStorage.useremail) {
      this.user.email = localStorage.useremail
    }
    let that = this
    let checkGauthLoad = setInterval(function(){
      that.isInit = that.$gAuth.isInit
      that.isSignIn = that.$gAuth.isAuthorized
      if(that.isInit) clearInterval(checkGauthLoad)
    }, 1000);
  }
  
}
</script>