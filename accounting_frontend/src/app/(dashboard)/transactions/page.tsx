"use client"

import { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Plus } from "lucide-react"
import api from "@/lib/api"

export default function TransactionsPage() {
    const [vouchers, setVouchers] = useState([])

    useEffect(() => {
        const fetchVouchers = async () => {
            try {
                const response = await api.get('/transactions/vouchers/')
                setVouchers(response.data)
            } catch (error) {
                console.error("Failed to fetch vouchers", error)
            }
        }
        fetchVouchers()
    }, [])

    return (
        <div className="grid gap-4">
            <div className="flex items-center justify-between">
                <h1 className="text-2xl font-bold">Transactions</h1>
                <Button>
                    <Plus className="mr-2 h-4 w-4" /> Create Voucher
                </Button>
            </div>
            <Card>
                <CardHeader>
                    <CardTitle>Recent Vouchers</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="relative w-full overflow-auto">
                        <table className="w-full caption-bottom text-sm">
                            <thead className="[&_tr]:border-b">
                                <tr className="border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted">
                                    <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Date</th>
                                    <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Voucher No</th>
                                    <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Type</th>
                                    <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Status</th>
                                </tr>
                            </thead>
                            <tbody className="[&_tr:last-child]:border-0">
                                {vouchers.map((voucher: any) => (
                                    <tr key={voucher.id} className="border-b transition-colors hover:bg-muted/50">
                                        <td className="p-4 align-middle font-medium">{voucher.date}</td>
                                        <td className="p-4 align-middle">{voucher.voucher_number}</td>
                                        <td className="p-4 align-middle">{voucher.voucher_type}</td>
                                        <td className="p-4 align-middle">
                                            <span className={`px-2 py-1 rounded-full text-xs ${voucher.status === 'POSTED' ? 'bg-green-100 text-green-800' :
                                                    voucher.status === 'CANCELLED' ? 'bg-red-100 text-red-800' : 'bg-gray-100 text-gray-800'
                                                }`}>
                                                {voucher.status}
                                            </span>
                                        </td>
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
