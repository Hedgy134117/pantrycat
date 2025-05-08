import Recipe from "./Recipe";

export default async function Page() {
    console.log(process.env.NEXT_PUBLIC_LOCAL);
    const res = await fetch(`${process.env.NEXT_PUBLIC_LOCAL}`);
    const data = await res.json();
    return data.map((recipe: [number, string, string]) => {
        return <Recipe key={recipe[1]} name={recipe[1]} source={recipe[2]} />
    })
}