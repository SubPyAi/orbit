import { toast } from "sonner";

const APIVersionEndpoint = "http://127.0.0.1:8000/api/version";
export let APIURL = "";

type JSONData = Record<string, unknown>;

export async function setAPI() {
    try{
        const res = await fetch(APIVersionEndpoint);
        const data = await res.json()
        console.log(data)
        APIURL = APIVersionEndpoint.replace("version", "") + data.version;
        console.log(APIURL);
        return 0
    }
    catch (e) {
        console.log(e)
        return 1;
    }
};

async function sendAPIReq(req: string, method: string, body: JSONData) {
    try {
        const res = await fetch(APIURL+req, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)
        });
        console.log(JSON.stringify(body));
        const data = await res.json();
        return data;
    } catch (e) {
        toast.error("Our servers are facing some issues at the moment, maybe try later??")
        return {"status": -1, "data": e};
    }
}

export async function SendCreateUserReq(userData: JSONData) {
    console.log("beginapi")
    const email = userData.email;
    const password = userData.password;
    const DoB = userData.DoB;
    const phone = userData.phone;
    const username = userData.username;
    const pfp_ref = userData.pfp_ref;
    const api_res = await sendAPIReq("/signup/create", "POST", {"username": username, "password": password, "email": email, "phone": phone, "DoB": DoB, "pfp_ref": pfp_ref});
    console.log("api response to signup: ", api_res);
    return api_res;
};

export async function SendLoginReq(userData: JSONData) {
    const username = userData.username;
    const password = userData.password;
    const api_res = await sendAPIReq("/auth/login", "POST", {"username": username, "password": password})
    return api_res;
}