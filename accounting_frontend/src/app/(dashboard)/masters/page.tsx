"use client"

import { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Plus } from "lucide-react"
import api from "@/lib/api"

export default function MastersPage() {
    const [ledgers, setLedgers] = useState([])

    useEffect(() => {
        const fetchLedgers = async () => {
            try {
                const response = await api.get('/masters/ledgers/')
                setLedgers(response.data)
            } catch (error) {
                console.error("Failed to fetch ledgers", error)
            }
        }
        fetchLedgers()
    }, [])

    return (
        <div className="grid gap-4">
            <div className="flex items-center justify-between">
                <h1 className="text-2xl font-bold">Masters</h1>
                <Button>
                    <Plus className="mr-2 h-4 w-4" /> Add Ledger
                </Button>
            </div>
            <Card>
                <CardHeader>
                    <CardTitle>Ledgers</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="relative w-full overflow-auto">
                        <table className="w-full caption-bottom text-sm">
                            <thead className="[&_tr]:border-b">
                                <tr className="border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted">
                                    <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Name</th>
                                    <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Group</th>
                                    <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">GSTIN</th>
                                    <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">State</th>
                                </tr>
                            </thead>
                            <tbody className="[&_tr:last-child]:border-0">
                                {ledgers.map((ledger: any) => (
                                    <tr key={ledger.id} className="border-b transition-colors hover:bg-muted/50">
                                        <td className="p-4 align-middle font-medium">{ledger.name}</td>
                                        <td className="p-4 align-middle">{ledger.group_name}</td>
                                        <td className="p-4 align-middle">{ledger.gstin || '-'}</td>
                                        <td className="p-4 align-middle">{ledger.state_code || '-'}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}
