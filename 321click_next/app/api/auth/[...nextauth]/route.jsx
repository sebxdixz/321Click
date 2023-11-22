import NextAuth from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import axios from "../../../../lib/axios";
//authenticates user login with credentials from flask api

export const authOptions = {
    providers: [
        CredentialsProvider({
        name: "Credentials",
        credentials: {
            email: {
            label: "Email",
            type: "email",
            placeholder: "email",
            },
            password: {
            label: "Password",
            type: "password",
            placeholder: "password",
            },
        },
        async authorize(credentials) {
            try {
            const res = await axios.post("/api/empleado/login", credentials);
            if (res.data.error) {
                try {
                    const res = await axios.post("/api/empleador/login", credentials);
                    if (res.data.error) {
                        console.log(res.data.error);
                        throw new Error(res.data.error);
                    } else {
                        return res.data;
                    }
                    } catch (error) {
                    throw new Error(error.message);
                    }
            } else {
                try {
                    const res = await axios.post("/api/empleador/login", credentials);
                    if (res.data.error) {
                        console.log(res.data.error);
                        throw new Error(res.data.error);
                    } else {
                        return res.data;
                    }
                    } catch (error) {
                    throw new Error(error.message);
                    }
                return res.data;
            }
            } catch (error) {
                try {
                    const res = await axios.post("/api/empleador/login", credentials);
                    if (res.data.error) {
                        console.log(res.data.error);
                        throw new Error(res.data.error);
                    } else {
                        return res.data;
                    }
                    } catch (error) {
                    throw new Error(error.message);
                    }
            throw new Error(error.message);
            }
        },
        }),
    ],
    pages: {
        signIn: "/login",
    },
    callbacks: {
        async jwt(token, user) {
        if (user) {
            token.accessToken = user.accessToken;
            token.user = user.user;
        }
        return token;
        },
        async session(session, token) {
        session.accessToken = token.accessToken;
        session.user = token.user;
        return session;
        },
    },
    };

const handler = NextAuth(authOptions);

export { handler as GET, handler as POST };