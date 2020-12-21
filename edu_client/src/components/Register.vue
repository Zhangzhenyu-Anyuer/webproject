<template>
    <div class="box">
        <img src="../../static/image/1111.jpg" alt="">
        <div class="register">
            <div class="register_box">
                <div class="register-title">百知教育在线平台注册</div>
                <div class="inp">
                    <input v-model="phone" type="text" placeholder="手机号码" class="user" @blur="check_phone">
                    <input v-model="password" type="password" placeholder="登录密码" class="user">
                    <div id="geetest"></div>
                    <div class="sms-box">
                        <input v-model="code" type="text" maxlength="6" placeholder="请输入验证码" class="user">
                        <div class="sms-btn" v-if="show" @click="get_code">获取验证码</div>
                        <div class="sms-btn" v-if="!show">{{ times }}s</div>

                    </div>
                    <button class="register_btn" @click="regist">注册</button>
                    <p class="go_login">已有账号
                        <!--                                                <router-link to="/login">直接登录</router-link>-->
                        <span><router-link to="/login">直接登录</router-link></span>
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "Register",
    data() {
        return {
            phone: '',
            password: '',
            code: '',
            times:60,
            show: true,
        }
    },
    methods: {
        get_code() {
            this.$axios({
                url: this.$settings.HOST + 'user/send/',
                method: "get",
                params: {
                    phone: this.phone
                }
            }).then(res => {
                this.$message({
                    message: res.data.message,
                    type: "success",
                    duration: 1000,
                })
                // TODO 倒计时
                this.show = false
                this.timer = setInterval(()=>{
                    this.times--
                    if(this.times===0){
                        this.show = true
                        clearInterval(this.timer)
                    }
                },1000)
            }).catch(error => {
                this.$message({
                    message: error.data.message,
                    type: "error",
                    duration: 1000,
                })

            })
        },
        regist() {
            this.$axios({
                url: this.$settings.HOST + 'user/register/',
                method: "post",
                data: {
                    phone: this.phone,
                    password: this.password,
                    code: this.code,
                }
            }).then(res => {
                this.$message({
                    message: '注册成功',
                    type: "success",
                    duration: 1000,
                })
                console.log(res.data.token);
                sessionStorage.token = res.data.token;
                this.$router.push('/')
            }).catch(error => {
                this.$message({
                    message: '注册失败',
                    type: "warning",
                    duration: 1000,
                })
            })
        },
        check_phone() {
            if (this.phone) {
                console.log('发送请求验证手机号码');
                this.$axios({
                    url: this.$settings.HOST + 'user/check/',
                    method: 'get',
                    params: {
                        phone: this.phone
                    }
                }).then(res => {
                    console.log(res);
                }).catch(error => {
                    this.$message({
                        message: error.response.data.message,
                        type: "warning",
                        duration: 1000,
                    })
                })
            } else {
                console.log('未进行验证手机号');
            }
        }
    }
}
</script>

<style scoped>
.box {
    width: 100%;
    height: 100%;
    position: relative;
    overflow: hidden;
}

.box img {
    width: 100%;
    min-height: 100%;
}

.box .register {
    position: absolute;
    width: 500px;
    height: 400px;
    top: 0;
    left: 0;
    margin: auto;
    right: 0;
    bottom: 0;
    top: -338px;
}

.register .register-title {
    width: 100%;
    font-size: 24px;
    text-align: center;
    padding-top: 30px;
    padding-bottom: 30px;
    color: #4a4a4a;
    letter-spacing: .39px;
}

.register-title img {
    width: 190px;
    height: auto;
}

.register-title p {
    font-family: PingFangSC-Regular;
    font-size: 18px;
    color: #fff;
    letter-spacing: .29px;
    padding-top: 10px;
    padding-bottom: 50px;
}

.register_box {
    width: 400px;
    height: auto;
    background: #fff;
    box-shadow: 0 2px 4px 0 rgba(0, 0, 0, .5);
    border-radius: 4px;
    margin: 0 auto;
    padding-bottom: 40px;
}

.register_box .title {
    font-size: 20px;
    color: #9b9b9b;
    letter-spacing: .32px;
    border-bottom: 1px solid #e6e6e6;
    display: flex;
    justify-content: space-around;
    padding: 50px 60px 0 60px;
    margin-bottom: 20px;
    cursor: pointer;
}

.register_box .title span:nth-of-type(1) {
    color: #4a4a4a;
    border-bottom: 2px solid #84cc39;
}

.inp {
    width: 350px;
    margin: 0 auto;
}

.inp input {
    border: 0;
    outline: 0;
    width: 100%;
    height: 45px;
    border-radius: 4px;
    border: 1px solid #d9d9d9;
    text-indent: 20px;
    font-size: 14px;
    background: #fff !important;
}

.inp input.user {
    margin-bottom: 16px;
}

.inp .rember {
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    margin-top: 10px;
}

.inp .rember p:first-of-type {
    font-size: 12px;
    color: #4a4a4a;
    letter-spacing: .19px;
    margin-left: 22px;
    display: -ms-flexbox;
    display: flex;
    -ms-flex-align: center;
    align-items: center;
    /*position: relative;*/
}

.inp .rember p:nth-of-type(2) {
    font-size: 14px;
    color: #9b9b9b;
    letter-spacing: .19px;
    cursor: pointer;
}

.inp .rember input {
    outline: 0;
    width: 30px;
    height: 45px;
    border-radius: 4px;
    border: 1px solid #d9d9d9;
    text-indent: 20px;
    font-size: 14px;
    background: #fff !important;
}

.inp .rember p span {
    display: inline-block;
    font-size: 12px;
    width: 100px;
    /*position: absolute;*/
    /*left: 20px;*/

}

#geetest {
    margin-top: 20px;
}

.register_btn {
    width: 100%;
    height: 45px;
    background: #84cc39;
    border-radius: 5px;
    font-size: 16px;
    color: #fff;
    letter-spacing: .26px;
    margin-top: 30px;
}

.inp .go_login {
    text-align: center;
    font-size: 14px;
    color: #9b9b9b;
    letter-spacing: .26px;
    padding-top: 20px;
}

.inp .go_login span {
    color: #84cc39;
    cursor: pointer;
}

.sms-box {
    position: relative;
}

.sms-btn {
    font-size: 14px;
    color: #ffc210;
    letter-spacing: .26px;
    position: absolute;
    right: 16px;
    top: 10px;
    cursor: pointer;
    overflow: hidden;
    background: #fff;
    border-left: 1px solid #484848;
    padding-left: 16px;
    padding-bottom: 4px;
}
</style>
