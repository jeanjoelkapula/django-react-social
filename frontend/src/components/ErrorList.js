import React from "react";

export default function ErrorList (props) {
    console.log(props.errors);
    var key_list = Object.keys(props.errors);

    var error_list = [];

    key_list.forEach(key => {
        error_list = props.errors[key].map((error, index) => {
            return (
                <li key={index}>
                    {error}
                </li>
            );
        });
    });

    return (
        <ul>
            {error_list}
        </ul>
    )
}