import { ApolloClient, HttpLink, InMemoryCache } from "@apollo/client"


export const createApolloClient = ( authToken?: string) => {
  return new ApolloClient({
    link: new HttpLink({
      uri: "http://localhost:8000/graphql",
      headers: authToken ? { Authorization: `Bearer ${authToken}` } : {} 
    }),
    cache: new InMemoryCache()
  })
}