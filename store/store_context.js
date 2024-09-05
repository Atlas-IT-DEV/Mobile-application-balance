import { useContext, createContext } from "react";

import RootStore from "./root_store";

export const RootStoreContext = createContext(RootStore)

export const useStores = () => {
    const context = useContext(RootStoreContext)
    return context
}  
