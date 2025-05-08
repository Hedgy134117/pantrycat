export default function Recipe({ name, source }: { name: string, source: string }) {
    return <h1><a href={source}>{name}</a></h1>
}