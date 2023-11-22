// Page for redirecting to login or home page depending on if user is logged in or not
import { authOptions } from "./api/auth/[...nextauth]/route"
import { getServerSession } from 'next-auth/next'
import { redirect } from 'next/navigation'


export default async function Home() {
    const session = await getServerSession(authOptions)
    if (session) {
        redirect('/', { res })
    } else {
        redirect('/login', { res })
    }
    return <></>
}
