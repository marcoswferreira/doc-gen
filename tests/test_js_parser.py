"""
Testes unitários para o analisador de código JavaScript e TypeScript.
"""

import unittest
import tempfile
from pathlib import Path

from docgen.models import FileInfo, SymbolType
from docgen.parsers.js_ts_parser import JsTsParser


class TestJsTsParser(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.parser = JsTsParser()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_parse_typescript_interfaces_and_classes(self):
        code = '''
import { BaseEntity } from './base';

/**
 * Interface do usuario
 */
export interface IUser {
  id: string;
  name: string;
}

export class UserService extends BaseEntity {
  /**
   * Busca usuario por id
   */
  async findById(id: string): Promise<IUser> {
    return { id, name: 'Alice' };
  }
}

export const calculateDiscount = (total: number, percent: number = 0.1): number => {
  return total * (1 - percent);
};
'''
        file_path = self.root / "users.ts"
        file_path.write_text(code, encoding="utf-8")

        f_info = FileInfo(
            path="users.ts",
            absolute_path=str(file_path),
            language="TypeScript",
        )

        parsed = self.parser.parse(f_info)

        # Checa import
        self.assertEqual(len(parsed.imports), 1)
        self.assertTrue(parsed.imports[0].is_internal)

        # Checa símbolos
        names = [s.name for s in parsed.symbols]
        self.assertIn("IUser", names)
        self.assertIn("UserService", names)
        self.assertIn("calculateDiscount", names)

        # Checa interface
        if_symbol = next(s for s in parsed.symbols if s.name == "IUser")
        self.assertEqual(if_symbol.symbol_type, SymbolType.INTERFACE)
        self.assertIn("Interface do usuario", if_symbol.docstring)

        # Checa arrow function
        fn_symbol = next(s for s in parsed.symbols if s.name == "calculateDiscount")
        self.assertEqual(fn_symbol.symbol_type, SymbolType.FUNCTION)
        self.assertEqual(len(fn_symbol.parameters), 2)
        self.assertEqual(fn_symbol.parameters[0].name, "total")
        self.assertEqual(fn_symbol.parameters[0].type_annotation, "number")

    def test_parse_express_routes(self):
        code = '''
app.get('/api/health', (req, res) => {
  res.send('OK');
});

router.post('/api/orders', createOrder);
'''
        file_path = self.root / "routes.js"
        file_path.write_text(code, encoding="utf-8")

        f_info = FileInfo(
            path="routes.js",
            absolute_path=str(file_path),
            language="JavaScript",
        )

        parsed = self.parser.parse(f_info)
        routes = [s for s in parsed.symbols if s.symbol_type == SymbolType.ROUTE]
        self.assertEqual(len(routes), 2)
        self.assertEqual(routes[0].route_method, "GET")
        self.assertEqual(routes[0].route_path, "/api/health")
        self.assertEqual(routes[1].route_method, "POST")
        self.assertEqual(routes[1].route_path, "/api/orders")


if __name__ == "__main__":
    unittest.main()
