import React from "react"
import { reduxForm, Field } from 'redux-form';
import {Link} from "react-router-dom";
import { useEffect } from "react";
import {useSelector, useDispatch} from "react-redux";
import {setAuthLoading, setAuthMessage} from "../../redux/authForm";

let LoginForm = props => {
    
    const { handleSubmit, pristine, submitting  } = props;
    const authFormData = useSelector(state => state.authFormData);
    const dispatch = useDispatch();

    useEffect(()=>{
        dispatch(setAuthLoading(false));
        dispatch(setAuthMessage(null));

    },[]);

    
    return (
        <form className="auth-form validate-form" onSubmit={handleSubmit}>
            <span className="auth-form-logo">
                <i className="zmdi zmdi-landscape" style={{color: "black"}}></i>
            </span>

            <span className="auth-form-title p-b-34 p-t-27">
                Log in
            </span>

            <div className="wrap-input100 validate-Field" data-validate="Enter username">
                <Field className="input100" component="input" type="text"  name="username" placeholder="Username" />
                <span className="focus-input100" data-placeholder=""></span>
            </div>

            <div className="wrap-input100 validate-Field" data-validate="Enter password">
                <Field className="input100" component="input" type="password" name="password" placeholder="Password" />
                <span className="focus-input100" data-placeholder=""></span>
            </div>
            
            <div className="container-auth-form-btn">
                <button className="auth-form-btn" type="submit" disabled={pristine || submitting}>
                    Login
                </button>
            </div>

            <div className="text-center p-t-90">
                <Link className="txt1" to="/register">
                    Don't have an account yet? Register
                </Link>
            </div>
        </form>

    )
}

LoginForm = reduxForm({
    form: 'loginForm'
})(LoginForm)

export default LoginForm