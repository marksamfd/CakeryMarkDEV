

function resetPassword({params}) {
    const token = (await params).token;
    async function resetPassswordForm(fd){
        

        const order = await (
          await fetch(`${process.env.backend}/user/baker/orders`, {
            headers: {
              Authorization: `Bearer ${token}`,
              Accept: 'application/json',
              'Content-Type': 'application/json',
            },
          })
        ).json();
    }
    return (
<></>
    )
}

export default resetPassword
